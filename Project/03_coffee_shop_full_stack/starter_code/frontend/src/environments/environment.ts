export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-jmfhs3otmbnizsez.us', // the auth0 domain prefix
    audience: 'https://coffee-shop-api/', // the audience set for the auth0 app
    clientId: 'oz7AeeczE0vRlyqI89oK42ox68kHDDL9', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
