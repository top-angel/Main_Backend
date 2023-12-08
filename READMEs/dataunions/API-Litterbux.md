# Litterbux apis

### Guild Management API

#### Create Guild

```bash
curl --location --request POST 'https://crab.litterbux.dataunion.app/guild/create' \
--header 'Authorization: Bearer <access_token>' \
--form 'file=@"profile.jpg"' \
--form 'invited_users="[]"' \
--form 'name="guild_name"' \
--form 'description="guild_description"' \
--form 'file-type="image"'
```

#### Join Guild

```bash
curl --location --request GET 'https://crab.litterbux.dataunion.app/guild/join?guild_id=[GUILD_ID]'
```


#### Leave Guild

```bash
curl --location --request GET 'https://crab.litterbux.dataunion.app/guild/leave?guild_id=[GUILD_ID]'
```

#### Fetch Guild List

```bash
curl --location --request GET 'https://crab.litterbux.dataunion.app/guild/list'
```


#### Get Guild Info By Guild Id
```bash
curl --location --request GET 'https://crab.litterbux.dataunion.app/guild/?guild_id=[GUILD_ID]'
```
