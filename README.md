<a href="../../"><img src="./images/badge.png?raw=true" width="128"></a><br>
<div align="left">
  
[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](../../wiki/ "Go to project documentation")

</div>

# EasyAsPermissions
A plugin for [Endstone](https://github.com/EndstoneMC/endstone) that allows you to manage player permissions without any programming!

# Installation
1) Download the latest [release](../../releases).
2) Drag and drop both files ending with `.whl` into your Endstone plugin folder.
3) Restart or reload your server. Enjoy!

### Demo
<img src="./images/mdemo.png?raw=true">

# Features
- ## Manager UI
  - Create, remove, and edit permissions using a simple UI.
  - Manage player roles.
- ## Roles UI
  - Setup and apply roles/groups containing multiple permissions to players.

# Commands
- `/permsmanager` - `easyas.permissions.manager`
- `/resetpermissions` - `easyas.permissions.reset`
- `/perm` - `easyas.command.perm`
- `/role` - `easyas.command.role`

# Tutorial
### *Using In-Game UI*
1) With **operator** or the `easyas.permissions.manager` permission, run the `/permsmanager` command.
2) This is where you can add, remove, and edit existing permissions, roles, and players.
   - Next click 'Add Permission'.
3) Here you can configure all of the different attributes of your new permission.
   - For more information, refer to the wiki page, [COMING_SOON](../../wiki/Command-Attributes).
   - Try creating the following permission:
     - Set the name to '`custom.command.star`'.
     - Set the default access to '`op`'.
5) Click **Submit**, and your server will reload to apply your new permission.
6) Now let's give you the permission; Open the manager back up and click 'Edit Player'.
7) Here you can manage an individual player's permissions and roles.
   - Enter your name, and hit **Submit**.
   - Click 'Add Permission', and enter '`custom.command.star`'.
   - Click **Submit**.
9) You will now have access to anything that configure to use the `custom.command.star` permission!
   > - This plugin does not provide uses for permissions; to use them with commands, consider trying **[EasyAsCommands](../../../EasyAsCommands/)**.
   > - Feel free to remove it if you don't want it by repeating the steps using 'Remove', or using the '`/resetpermissions`' command.

### *Using JSON Editor*
1) For more advanced users, a more efficient approach is to edit the JSON directly.
To start, navigate to your `/bedrock_server/config/` folder; the `/config/` folder should be in the same directory as your `/plugins/` folder.
2) Open `permissions_manager.json` in your choice of text editor. You don't need anything fancy; Notepad will do.
3) Begin editing. Refer to the wiki page [COMING_SOON](../../wiki/JSON-Arguments) for available arguments.
Once done, save the file and reload/restart your server for the changes to take effect.

### 🥳 Congratulations!
You've created your first permissions!

I hope you find this plugin useful! Enjoy!

# Feature Roadmap
**Feature**|**Status**
:-----:|:-----:
Permissions Manager UI|✅
Role Manager UI|✅
Reset command|✅
Permission commands|✅
Documentation|🔷
Developer API|🔷

✅ - Complete
🔷 - Work in Progress
🔶 - Planned

## Feedback
If you experience any issues or have a suggestion, please create an [Issue](../../issues), and I'll try to get to it when I can!
