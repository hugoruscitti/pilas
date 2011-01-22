import weakref

from pilas.dispatch import saferef

WEAKREF_TYPES = (weakref.ReferenceType, saferef.BoundMethodWeakref)


class DictObj(object):
    def __init__(self, d):
        self.d = d

    def __getattr__(self, m):
        return self.d.get(m, None)
    
    def __str__(self):
        return "<Evento %s>" %(str(self.d))

def _make_id(target):
    if hasattr(target, 'im_func'):
        return (id(target.im_self), id(target.im_func))
    return id(target)

class Signal(object):
    """
    Base class for all signals
    
    Internal attributes:
    
        receivers
            { receriverkey (id) : weakref(receiver) }
    """
    
    def __init__(self, providing_args=None):
        """
        Create a new signal.
        
        providing_args
            A list of the arguments this signal can pass along in a send() call.
        """
        self.receivers = []
        if providing_args is None:
            providing_args = []
        self.providing_args = set(providing_args)

    def conectar(self, receptor, emisor=None, weak=True, uid=None):
        return self.connect(receptor, emisor, weak, uid)

    def connect(self, receiver, sender=None, weak=True, uid=None):
        """
        Connect receiver to sender for signal.
    
        Arguments:
        
            receiver
                A function or an instance method which is to receive signals.
                Receivers must be hashable objects.

                if weak is True, then receiver must be weak-referencable (more
                precisely saferef.safeRef() must be able to create a reference
                to the receiver).
        
                Receivers must be able to accept keyword arguments.

                If receivers have a uid attribute, the receiver will
                not be added if another receiver already exists with that
                uid.

            sender
                The sender to which the receiver should respond Must either be
                of type Signal, or None to receive events from any sender.

            weak
                Whether to use weak references to the receiver By default, the
                module will attempt to use weak references to the receiver
                objects. If this parameter is false, then strong references will
                be used.
        
            uid
                An identifier used to uniquely identify a particular instance of
                a receiver. This will usually be a string, though it may be
                anything hashable.
        """
        
        if uid:
            lookup_key = (uid, _make_id(sender))
        else:
            lookup_key = (_make_id(receiver), _make_id(sender))

        if weak:
            receiver = saferef.safeRef(receiver, onDelete=self._remove_receiver)

        for r_key, _ in self.receivers:
            if r_key == lookup_key:
                break
        else:
            self.receivers.append((lookup_key, receiver))

    def desconectar(self, receptor=None, emisor=None, weak=True, uid=None):
        self.disconnect(receptor, emisor, weak, uid)

    def disconnect(self, receiver=None, sender=None, weak=True, uid=None):
        """
        Disconnect receiver from sender for signal.

        If weak references are used, disconnect need not be called. The receiver
        will be remove from dispatch automatically.
    
        Arguments:
        
            receiver
                The registered receiver to disconnect. May be none if
                uid is specified.
            
            sender
                The registered sender to disconnect
            
            weak
                The weakref state to disconnect
            
            uid
                the unique identifier of the receiver to disconnect
        """
        if uid:
            lookup_key = (uid, _make_id(sender))
        else:
            lookup_key = (_make_id(receiver), _make_id(sender))
        
        for index in xrange(len(self.receivers)):
            (r_key, _) = self.receivers[index]
            if r_key == lookup_key:
                del self.receivers[index]
                break

    def send(self, sender, **named):
        """
        Send signal from sender to all connected receivers.

        If any receiver raises an error, the error propagates back through send,
        terminating the dispatch loop, so it is quite possible to not have all
        receivers called if a raises an error.

        Arguments:
        
            sender
                The sender of the signal Either a specific object or None.
    
            named
                Named arguments which will be passed to receivers.

        Returns a list of tuple pairs [(receiver, response), ... ].
        """
        responses = []
        if not self.receivers:
            return responses

        for receiver in self._live_receivers(_make_id(sender)):
            response = receiver(DictObj(named))
            responses.append((receiver, response))
        return responses

    def send_robust(self, sender, **named):
        """
        Send signal from sender to all connected receivers catching errors.

        Arguments:
        
            sender
                The sender of the signal Can be any python object (normally one
                registered with a connect if you actually want something to
                occur).

            named
                Named arguments which will be passed to receivers. These
                arguments must be a subset of the argument names defined in
                providing_args.

        Return a list of tuple pairs [(receiver, response), ... ]. May raise
        DispatcherKeyError.

        if any receiver raises an error (specifically any subclass of
        Exception), the error instance is returned as the result for that
        receiver.
        """
        responses = []
        if not self.receivers:
            return responses

        # Call each receiver with whatever arguments it can accept.
        # Return a list of tuple pairs [(receiver, response), ... ].
        for receiver in self._live_receivers(_make_id(sender)):
            try:
                response = receiver(signal=self, sender=sender, **named)
            except Exception, err:
                responses.append((receiver, err))
            else:
                responses.append((receiver, response))
        return responses

    def _live_receivers(self, senderkey):
        """
        Filter sequence of receivers to get resolved, live receivers.

        This checks for weak references and resolves them, then returning only
        live receivers.
        """
        none_senderkey = _make_id(None)
        receivers = []

        for (receiverkey, r_senderkey), receiver in self.receivers:
            if r_senderkey == none_senderkey or r_senderkey == senderkey:
                if isinstance(receiver, WEAKREF_TYPES):
                    # Dereference the weak reference.
                    receiver = receiver()
                    if receiver is not None:
                        receivers.append(receiver)
                else:
                    receivers.append(receiver)
        return receivers

    def _remove_receiver(self, receiver):
        """
        Remove dead receivers from connections.
        """

        to_remove = []
        for key, connected_receiver in self.receivers:
            if connected_receiver == receiver:
                to_remove.append(key)
        for key in to_remove:
            for idx, (r_key, _) in enumerate(self.receivers):
                if r_key == key:
                    del self.receivers[idx]

    def esta_conectado(self):
        "Indica si tiene alguna funcion conectada."
        return self.receivers
    
    def imprimir_funciones_conectadas(self):
        "Imprime todas las funciones que tiene conectado el evento."
        for clave, referencia in self.receivers:
            nombre = referencia.__str__()
            nombre = nombre[nombre.index('(')+1:nombre.index(")")]
            print "\t", nombre