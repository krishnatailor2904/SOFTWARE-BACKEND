# Krishna Tailor - Vercel Deploy Guide (Backend)

Ye backend aur frontend **do alag Vercel projects** ke roop me deploy karne
hain (ek hi repo me dono folders rakh sakte ho, bas "Root Directory" alag
select karna hoga har project me).

## Sabse important baat pehle

Vercel serverless hai - filesystem **ephemeral** hota hai. SQLite file
(`bill_data.sqlite3`) me kiya gaya koi bhi write agli request tak persist
NAHI karega. Isliye Postgres use karna zaroori hai (SQLite sirf local dev
ke liye hai).

Free Postgres 2 minute me mil jaata hai:
- **Neon** (neon.tech) - recommended, sabse fast setup
- **Supabase** (supabase.com)
- ya Vercel dashboard me "Storage -> Postgres" add karo

## Backend deploy steps

1. **Postgres banao** — Neon/Supabase pe account banao, connection string
   copy karo:
   `postgresql://user:password@host/dbname?sslmode=require`

2. **Is `backend` folder ko GitHub pe push karo** (agar frontend bhi usi
   repo me hai to koi baat nahi, alag folders me rehna chahiye).

3. **Vercel dashboard me "Add New Project" se import karo.**
   Root Directory setting me `backend` select karo (jahan `manage.py` hai
   wahi root hona chahiye).
   Vercel `manage.py` ko dekh ke Django ko khud hi detect kar lega — koi
   extra build command ya framework preset select karne ki zaroorat nahi.

4. **Environment Variables** (Project -> Settings -> Environment Variables):
   - `SECRET_KEY` -> koi bhi random 50-character string
   - `DEBUG` -> `False`
   - `DATABASE_URL` -> step 1 wali Postgres connection string

5. **Deploy karo.** Vercel apne aap `requirements.txt` install karega,
   static files collect karega, aur Django ko ek Vercel Function bana dega.

6. **Migrations run karo** — Vercel pe build ke time DB access nahi hota,
   isliye ek baar apne local machine se karna hoga, Postgres wale
   `DATABASE_URL` ko point karke:
   ```bash
   pip install -r requirements.txt
   # Windows: set DATABASE_URL=postgresql://...
   # Mac/Linux:
   export DATABASE_URL=postgresql://...
   python manage.py migrate
   python manage.py createsuperuser
   ```
   Isse Postgres DB tables ke saath ready ho jaayega aur admin login
   (`/admin/`) bhi ban jaayega.

7. **Check karo** — deploy hone ke baad apne backend ka URL kholo
   (`https://your-backend.vercel.app/`), `{"status": "ok", ...}` dikhna
   chahiye. Agar ye nahi dikha to backend hi deploy nahi hua theek se —
   Vercel ke "Deployments" tab me build logs check karo.

## Frontend ko connect karo (BEHAD ZAROORI STEP)

Backend deploy hone ke baad uska URL copy karo (jaise
`https://your-backend.vercel.app`). Frontend Vercel project me:

- **Settings -> Environment Variables** me add karo:
  ```
  VITE_API_URL = https://your-backend.vercel.app/api
  ```
  (`/api` lagana mat bhoolna — backend ke saare routes isi prefix ke peeche
  hain)
- Ye set kiye bina register/login/bill save — kuch bhi kaam nahi karega,
  kyunki frontend by default localhost pe hi call karega.
- Env var add/change karne ke baad frontend ko **redeploy** karna padega
  (Vercel "Redeploy" button, ya naya git push).

## CORS

`CORS_ALLOW_ALL_ORIGINS = True` already set hai settings.py me, isliye
frontend ka koi bhi Vercel domain backend ko call kar sakta hai — alag se
kuch add karne ki zaroorat nahi.

## Ek baat aur

Agar tumhe SQLite hi rakhna hai aur simple rehna hai, to Render pe (jo
pehle se configured hai - `render.yaml`, `build.sh`) deploy karna zyada
sahi rahega, kyunki wahan persistent disk milta hai. Vercel sirf tab
sahi choice hai jab Postgres use karne ko ready ho.
