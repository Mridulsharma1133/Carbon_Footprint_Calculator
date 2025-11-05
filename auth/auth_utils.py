from .supabase_client import supabase
import unicodedata

def safe_str(err):
    """Convert any error or object to a printable safe string."""
    try:
        text = unicodedata.normalize("NFKD", str(err))
        return text.encode("ascii", "ignore").decode("ascii")
    except Exception:
        return "Unexpected error (encoding issue)"


# ---------------- Register ----------------
def register_user(email: str, password: str):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        print("DEBUG: Supabase response recieved successfully.")

        # Convert everything safely before returning
        if hasattr(res, "error") and res.error:
            return None, safe_str(res.error.message)
        
        if isinstance(res, dict) and res.get("error"):
            return None, safe_str(res["error"])
        
        return res.user if hasattr(res, "user") else res, None

    except Exception as e:
        return None, safe_str(e)


# ---------------- Login ----------------
def login_user(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print("DEBUG: Supabase response received successfully.")

        if hasattr(res, "error") and res.error:
            return None, safe_str(res.error.message)
        
        if isinstance(res, dict) and res.get("error"):
            return None, safe_str(res["error"])
        
        return res, None

    except Exception as e:
        return None, safe_str(e)


# ---------------- Logout ----------------
def logout_user():
    try:
        supabase.auth.sign_out()
        return True
    except Exception as e:
        print("Logout error:", safe_str(e))
        return False
