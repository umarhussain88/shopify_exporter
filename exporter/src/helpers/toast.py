
from platform import platform

import platform


if platform.system() == 'Windows':

    import winrt.windows.ui.notifications as notifications
    import winrt.windows.data.xml.dom as dom


    def toast_builder(msg : str) -> None:
        app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

        #create notifier
        nManager = notifications.ToastNotificationManager
        notifier = nManager.create_toast_notifier(app)

        #define your notification as string

        #convert notification to an XmlDocument
        xDoc = dom.XmlDocument()
        xDoc.load_xml(msg)

        #display notification
        notifier.show(notifications.ToastNotification(xDoc))




else:

    def toast_builder():
        pass