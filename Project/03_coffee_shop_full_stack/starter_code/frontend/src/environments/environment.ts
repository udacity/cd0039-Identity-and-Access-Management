/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'webdevofficial', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: '62f56d028c6803fe0d3b04e6', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8100', // the base url of the running ionic application. 
    // changing this because of the following error; Error! Payload validaton error: 'Object didn't pass validation for format absoulte-uri-or-empty: https://localhost:5000/login on property initiate_login_uri(initiate login ur, just be https and cannot contain a fragment)
  }
};
