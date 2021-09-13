
from platform import platform

import platform


if platform.system() == 'Windows':

    import winrt.windows.ui.notifications as notifications
    import winrt.windows.data.xml.dom as dom
    from getpass import getuser
    from pathlib import Path 


    def file_not_find_toast(fp):
        app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

        #create notifier
        nManager = notifications.ToastNotificationManager
        notifier = nManager.create_toast_notifier(app)

        #define your notification as string
        tString = f"""
        <toast>
            <visual>
            <binding template='ToastGeneric'>
                <text>Shopify Export, File Not Found Error!</text>
                <text>Hi {getuser()} - {fp}\n is not a valid path - for help, please refer to the instructions.</text>
            </binding>
            </visual>
            <actions>
            <action
                content="Dismiss"
                arguments="action=dismiss"/>
            </actions>        
        </toast>
        """

        #convert notification to an XmlDocument
        xDoc = dom.XmlDocument()
        xDoc.load_xml(tString)

        #display notification
        notifier.show(notifications.ToastNotification(xDoc))
else:

    def file_not_find_toast():
        pass