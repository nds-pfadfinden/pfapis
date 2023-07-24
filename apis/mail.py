import smtplib, ssl


class EMailSender:
    """
    Thie Class provides a E-Mail sender to send Mails over smtp.
    @author Umberto Albano
    """

    def __init__(self, smtp_server: str, sender_email: str, password: str, port: int = 587) -> object:
        """

        @param smtp_server: URL of the stmtp server for sending mails
        @param sender_email: E-Mail of the sender aka. Username for login
        @param password: Password for loging at the smtp server
        @param port: Port ot the smtp service. (Default is 587)
        """
        context = ssl.create_default_context()
        self.__sender_email = sender_email
        try:
            self.__server = smtplib.SMTP(smtp_server, port)
            self.__server.ehlo()  # Can be omitted
            self.__server.starttls(context=context)  # Secure the connection
            self.__server.ehlo()  # Can be omitted
            print("Login to E-mMil server:", self.__server.login(sender_email, password))
        except Exception as e:
            print("Cannot login to E-Mail Server: ", e)

    def __del__(self):
        pass

    def send_mail(self, address: list, subject: str, content: str, your_name: str = None, reply_to: str = None) -> object:
        """

        @param address: List of recipients e-mail addresses
        @param subject: Subject of the E-Mail.
        @param content: E-Mail Content (body)
        @param your_name: Name of the Sender for showing in the E-Mail header. Default is None.
        @param reply_to: Separate reply-to address. Default is None.
        """
        message = ""
        message += f"SUBJECT: {subject}\n"
        if your_name: message += f"FROM: {your_name} <{self.__sender_email}>\n"
        if reply_to: message += f"REPLY-TO: {reply_to}"
        message += "\n"
        message += f"{content}"

        self.__server.sendmail(from_addr=self.__sender_email, to_addrs=address, msg=message.encode('utf-8'))
