function WriteIniVisible(isVisible)
{
   fso   = new ActiveXObject('Scripting.FileSystemObject');

   rfile = fso.OpenTextFile('proxy.ini', 1);
   content = rfile.ReadAll();
   rfile.Close()

   content = content.replace(/visible\s*=[^\r]*/ig, 'visible = ' + isVisible);

   wfile = fso.OpenTextFile('proxy.ini', 2);
   wfile.Write(content);
   wfile.Close();
}

function CreateShortcut(target_path)
{
   wsh = new ActiveXObject('WScript.Shell');
   link = wsh.CreateShortcut(wsh.SpecialFolders("Startup") + '\\PyFtpModule.lnk');
   link.TargetPath = target_path;
   link.WindowStyle = 7;
   link.Description = 'PyFtpModule';
   link.WorkingDirectory = wsh.CurrentDirectory;
   link.Save();
}

function main()
{
   wsh = new ActiveXObject('WScript.Shell');
   fso = new ActiveXObject('Scripting.FileSystemObject');
   CreateShortcut('"' + wsh.CurrentDirectory + '\\PyFtpModule.py"');

}

main();
