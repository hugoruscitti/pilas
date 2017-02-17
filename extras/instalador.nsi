;NSIS Modern User Interface
;Start Menu Folder Selection Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include LogicLib.nsh
  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "pilas-engine"
  OutFile "pilas-engine_1.4.10.exe"

  ;Default installation folder
  InstallDir "c:\pilas-engine"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "pilas-engine\pilas" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Variables

  Var StartMenuFolder

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING


;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY



  
  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Modern UI Test" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_RUN "$instdir\pilas-engine.exe"

!define MUI_PAGE_CUSTOMFUNCTION_SHOW ModifyRunCheckbox
!insertmacro MUI_PAGE_FINISH

Section "Maybe" SID_MAYBE
; File "pilas-engine.exe"
SectionEnd

Function ModifyRunCheckbox
${IfNot} ${SectionIsSelected} ${SID_MAYBE}
    SendMessage $mui.FinishPage.Run ${BM_SETCHECK} ${BST_UNCHECKED} 0
    EnableWindow $mui.FinishPage.Run 0
${EndIf}
FunctionEnd

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES


;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "Spanish"

;--------------------------------
;Installer Sections

Section "Dummy Section" SecDummy

  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  File "pilas-engine.exe"
  File /r "data"
  File /r "pilas"
  File /r "pilasengine"
  
  ;Store installation folder
  WriteRegStr HKCU "pilas-eingine\pilas" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\desinstalar.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\desinstalar.lnk" "$INSTDIR\desinstalar.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\pilas-engine.lnk" "$INSTDIR\pilas-engine.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    
  Delete "$SMPROGRAMS\$StartMenuFolder\desinstalar.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"
  
  DeleteRegKey /ifempty HKCU "Software\Modern UI Test"

SectionEnd
