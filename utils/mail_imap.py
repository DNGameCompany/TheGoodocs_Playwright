import imaplib
import email
from email.header import decode_header
import time
from bs4 import BeautifulSoup


class MailIMAP:
    def __init__(self, email_address: str = "d.aydogdiev@ukr.net", password: str = "VCzp7Df5zFiiPmtZ"):
        self.host = "imap.ukr.net"
        self.port = 993
        self.email_address = email_address
        self.password = password

    def verification_link(self, timeout_seconds: float = 30) -> str:
        """Шукає посилання для підтвердження email."""
        # У BS4 аналог a:contains() реалізується через CSS selector абоBS4 lambda
        css_selector = "a:-soup-contains('Please confirm your email address. Click here!')"
        return self._wait_for_email_link(css_selector, timeout_seconds)

    def reset_password_link(self, timeout_seconds: float = 30) -> str:
        """Шукає посилання для скидання пароля."""
        href_contains = "&utm_campaign=reset-password"
        css_selector = f'a[href*="{href_contains}"]'
        return self._wait_for_email_link(css_selector, timeout_seconds)

    def _wait_for_email_link(self, css_selector: str, timeout_seconds: float) -> str:
        start_time = time.time()
        poll_interval = 5.0  # перевірка кожні 5 секунд

        print("[MailIMAP] Старт перевірки пошти...")

        while (time.time() - start_time) < timeout_seconds:
            try:
                # Підключаємося до IMAP SSL
                mail = imaplib.IMAP4_SSL(self.host, self.port)
                mail.login(self.email_address, self.password)
                mail.select("INBOX")

                # Отримуємо список всіх ID листів
                status, messages = mail.search(None, "ALL")
                if status == "OK":
                    email_ids = messages[0].split()

                    # Перевіряємо з останніх (від найновіших до найстаріших)
                    for email_id in reversed(email_ids):
                        status, msg_data = mail.fetch(email_id, "(RFC822)")
                        if status != "OK":
                            continue

                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                html_body = self._extract_html_body(msg)

                                if html_body:
                                    soup = BeautifulSoup(html_body, "html.parser")
                                    element = soup.select_one(css_selector)

                                    if element and element.has_attr("href"):
                                        url = element["href"]
                                        print(f"[MailIMAP] ✅ Знайдено посилання: {url}")

                                        # Позначаємо лист на видалення та очищаємо
                                        mail.store(email_id, "+FLAGS", "\\Deleted")
                                        mail.expunge()

                                        mail.close()
                                        mail.logout()
                                        return url

                mail.close()
                mail.logout()

            except Exception as e:
                print(f"[MailIMAP] Помилка під час обробки IMAP: {e}")

            print("[MailIMAP] ⏳ Лист не знайдено, чекаємо...")
            time.sleep(poll_interval)

        print("[MailIMAP] ❌ Час очікування вийшов, посилання не знайдено.")
        return ""

    def _extract_html_body(self, msg: email.message.Message) -> str:
        """Допоміжний метод для витягування HTML тіла листа."""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/html" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
        else:
            if msg.get_content_type() == "text/html":
                payload = msg.get_payload(decode=True)
                if payload:
                    return payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")

        return ""

    def delete_all_emails(self) -> None:
        """Видаляє всі листи з папки INBOX."""
        try:
            mail = imaplib.IMAP4_SSL(self.host, self.port)
            mail.login(self.email_address, self.password)
            mail.select("INBOX")

            status, messages = mail.search(None, "ALL")
            if status == "OK":
                email_ids = messages[0].split()
                print(f"[MailIMAP] Видалення {len(email_ids)} листів...")

                for email_id in email_ids:
                    mail.store(email_id, "+FLAGS", "\\Deleted")

                mail.expunge()
                print("[MailIMAP] ✅ Усі листи видалено.")

            mail.close()
            mail.logout()

        except Exception as e:
            print(f"[MailIMAP] Помилка при видаленні листів: {e}")