Flow: 

1. Frontend must check if user is already registered using /register api.
Input Body:
{
public_address: '0x123....'
}

If not found, 

return 200 with a nonce.

If found:

return 400 saying user already exists.

2. Get the nonce.

If user already exists get the nonce from `/get-nonce` api 

else `/register` will give nonce. 

3. Ask user to sign the message (using some wallet).
Generate a signature.

4. Call /login to get the access token.
Send the signed message with the signature from the second step.
/login should only be called when
1. user's access_token/refresh_token is lost.
2. Or `refresh_token` is expired.

Return:
If signature is valid,
user gets an access_token and refresh_token.
access_token -> Valid for short time.
refresh_token -> valid for long time.

5. /refresh

This is used to get new access_token.


### Getting token from dev backend

1. Create dummy ethereum account.
2. login to dev server (206.81.26.71) using ssh.
3. run `docker exec -it crab_backend_dev bash`
4. run `python -m helpers.login`
4.a Enter public address (make sure no trailing spaces are entered)
4.b Enter private key (won't be visible in console)
5. Backend will print access_token and refresh_token if all goes well.