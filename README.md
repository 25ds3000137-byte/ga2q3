# CORS-aware Metrics API

## Deploy to Render
1. Upload these files to a new GitHub repository.
2. In Render, choose **New + → Web Service** and connect that repository.
3. Set build command to `pip install -r requirements.txt`.
4. Set start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
5. Add environment variable `STUDENT_EMAIL=25ds3000137@ds.study.iitm.ac.in`.
6. Deploy and copy the public service URL.

## Test
`https://YOUR-SERVICE.onrender.com/stats?values=1,2,3`

Allowed-origin preflight:
```bash
curl -i -X OPTIONS 'https://YOUR-SERVICE.onrender.com/stats' \
  -H 'Origin: https://dash-iykobw.example.com' \
  -H 'Access-Control-Request-Method: GET'
```

Disallowed-origin preflight:
```bash
curl -i -X OPTIONS 'https://YOUR-SERVICE.onrender.com/stats' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```

The disallowed-origin response should not include `Access-Control-Allow-Origin`.
