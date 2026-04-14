import os
import smtplib
import sqlite3
import subprocess

from langchain_core.tools import tool


@tool
def read_file(path: str) -> str:
    """Read the contents of a file at the given path."""
    try:
        with open(path) as f:
            return f.read(8192)
    except Exception as e:
        return f"Error: {e}"


@tool
def run_shell(cmd: str) -> str:
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error: {e}"


@tool
def query_database(sql: str) -> str:
    """Run a SQL query against the application database."""
    db_path = os.getenv("DB_PATH", "devassist.db")
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return str(rows[:50])
    except Exception as e:
        return f"Error: {e}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email on behalf of the user."""
    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "25"))
    sender = os.getenv("SMTP_FROM", "devassist@acme.internal")
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=5) as s:
            s.sendmail(sender, to, f"Subject: {subject}\n\n{body}")
        return f"Email sent to {to}"
    except Exception as e:
        return f"Email send failed (SMTP not configured): {e}"


@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"[search stub] Results for: {query}"


TOOLS = [read_file, run_shell, query_database, send_email, search_web]
