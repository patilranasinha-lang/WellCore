# Welcome email setup (Gmail)

New users (e.g. `parthkulkarni0007@gmail.com`) receive mail **at their signup address**.
Mail is **sent from** the Gmail in `MAIL_USERNAME` (not from the user's password).

## Why you did not get email

`MAIL_PASSWORD` is empty in `.env`. Without a **Gmail App Password**, nothing is sent.

## Fix (5 minutes)

1. Sign in to the **same Gmail** as `MAIL_USERNAME` in `.env` (e.g. `patilranasinha@gmail.com`).
2. Turn on **2-Step Verification**: https://myaccount.google.com/security
3. Create an **App Password**: https://myaccount.google.com/apppasswords  
   - App: Mail  
   - Device: Windows Computer  
4. Open `fitlife/.env` and set (no spaces in the password):

   ```
   MAIL_PASSWORD=abcdefghijklmnop
   ```

   Or put only the password in `fitlife/instance/mail_secret.txt` (one line).

5. **Restart Flask** (stop with Ctrl+C, run `flask run` again).

6. Test:

   ```powershell
   cd fitlife
   ..\venv\Scripts\python scripts\test_email.py your-test@gmail.com
   ```

7. Register again with a **new** email, or use **Resend welcome email** on the dashboard.

## Check spam

Welcome mail may land in **Spam** or **Promotions**.

## Send from a different Gmail

To send from `parthkulkarni0007@gmail.com`, set in `.env`:

```
MAIL_USERNAME=parthkulkarni0007@gmail.com
MAIL_DEFAULT_SENDER=parthkulkarni0007@gmail.com
MAIL_PASSWORD=<app password for THAT account>
```
