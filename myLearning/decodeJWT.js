function parseJwt (token) {
    // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript
   var base64Url = token.split('.')[1];
   var base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));

   return JSON.parse(base64);
};

parseJwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imp1aWNlcHJvIiwicGVybWlzc2lvbnMiOlsicG9zdDpqdWljZSJdfQ.7m6ukD61G--xjWGIJJNBRwVJkSrnKwfHOU5KrYEvLW8')