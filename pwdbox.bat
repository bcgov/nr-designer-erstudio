@Echo off
>%TEMP%\_$.vbs (Echo/
	Echo/ passwordbox^("Enter Passwords And Run Value"^)
	Echo/ Set wshShell = CreateObject^( "WScript.Shell" ^)
	Echo/ Set wshSystemEnv = wshShell.Environment^( "Process" ^)
	Echo/ source_code_path = "h:\ERStudioDesigner\designer-ers.py"
	Echo/ currentCommand = "cmd /c " ^& CHR^(34^) ^& source_code_path ^& CHR^(34^)
	Echo/ wshShell.run currentCommand,1,True
	Echo/
	Echo/' A function to present a Password dialog in a VBS ^(WSF^) script
	Echo/' Requires WScript version 5.1^+
	Echo/' Tom Lavedas ^<tlave...@hotmail.com^>
	Echo/
	Echo/Function PasswordBox^(sPrompt^)
	Echo/  Set wshShell = CreateObject^( "WScript.Shell" ^)
	Echo/  Set wshSystemEnv = wshShell.Environment^( "Process" ^)
	Echo/  set oIE = CreateObject^("InternetExplorer.Application"^)
	Echo/  With oIE
	Echo/    .ToolBar = False
	Echo/    .RegisterAsDropTarget = False   : .Navigate^("about:blank"^)
	Echo/    While .Busy : WScript.Sleep 100 : Wend
	Echo/    With .document
	Echo/      With .ParentWindow
	Echo/        if Instr^(.navigator.appVersion, "MSIE 6"^) = 0 Then
	Echo/          oIE.FullScreen = True
	Echo/          .resizeto 400,180
	Echo/          .moveto .screen.width/2-200, .screen.height/2-90
	Echo/        else
	Echo/          .resizeto 400,230
	Echo/          .moveto .screen.width/2-200, .screen.height/2-115
	Echo/        End if
	Echo/      End With
	Echo/      .Write^("<html><head><" ^& "script>bboxwait=true;</" ^& "script>" _
	Echo/       ^& "<title>Password _____________________________ </title>" _
	Echo/       ^& "</head><body bgColor=Silver scroll=no language=vbs" _
	Echo/       ^& " onkeypress=""if window.event.keycode=13 Then" _
	Echo/       ^& " bboxwait=false""><center><b> " ^& sPrompt ^& "<b> <p>" _
	Echo/       ^& "<table><tr><td> <b>Database Password</b></td><td>" _
	Echo/       ^& "<input type=password id=orapass>" _
	Echo/       ^& "</td><tr><td> <b>IDIR Password:</b></td><td>" _
	Echo/       ^& "<input type=password id=idirpass>" _
	Echo/       ^& "</td><tr><td> <b>Github Token:</b></td><td>" _
	Echo/       ^& "<input type=password id=gittoken>" _
	Echo/       ^& "</td><tr><td> <b>Run:</b></td><td>" _
	Echo/       ^& "<input type=text id=whichrun value='Y'></td></tr></table><br>" _
	Echo/       ^& "<button onclick=""bboxwait=false;""> Submit </button>" _
	Echo/       ^& "</center></body></html>"^)
	Echo/      .ParentWindow.document.body.style.borderStyle = "outset"
	Echo/      .ParentWindow.document.body.style.borderWidth = "3px"
	Echo/      
	Echo/      On Error Resume Next
	Echo/      Do While .parentWindow.bBoxWait
	Echo/      oIE.Visible = True
	Echo/      if Err Then Exit Do
	Echo/      WScript.Sleep 100
	Echo/      Loop
	Echo/      oIE.Visible = False
	Echo/      if Err Then
	Echo/        PasswordBox = "CANCELLED"
	Echo/      Else
	Echo/        PasswordBox = ARRAY^("DONE"^)
	Echo/        wshSystemEnv^( "ORAPASS" ^) = .all.orapass.value
	Echo/        wshSystemEnv^( "IDIRPASS" ^) = .all.idirpass.value
	Echo/        wshSystemEnv^( "GITTOKEN" ^) = .all.gittoken.value
	Echo/        wshSystemEnv^( "WHICHRUN" ^) = .all.whichrun.value
	Echo/      End if
	Echo/      On Error Goto 0
	Echo/    End With ' document
	Echo/  End With   ' IE
	Echo/End Function)
Cscript //NoLogo %TEMP%\_$.vbs
