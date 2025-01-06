# krolok.net - a s3 static website for pets 🐾

welcome to the goofiest pet photo gallery on the internet. this website is hosted on aws because why not? it’s free (except the domain). here’s how it works:

### 🛠️ how it’s hosted
- **s3 bucket**: all the pet pics live here. it’s public, so everyone can see your furry friends.
- **cloudfront**: makes everything fast and secure with https. also caches stuff so your site doesn’t crash when your cat goes viral.
- **route 53**: handles the domain (in my case `krolok.net`). `krolok.pics` used to be the domain, but it’s going away on **04.02.2025**. rip.

### 🐰 what’s a krolok?
fun fact: "krolok" is a strange pronunciation of **królik**, which is polish for "rabbit". 🐇

### 🐶 how to host your own
1. **get pet pics**: put them in an `images` directory, with subdirectories named after each pet. yes, your hamster needs its own folder.
2. **buy a domain**: use route 53 or whatever. just make sure it’s cute.
3. **set up s3**:
   - create a bucket with public access. make it the same name as your domain/subdomain.
   - slap this bucket policy on it:
     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Principal": "*",
                 "Action": "s3:GetObject",
                 "Resource": "arn:aws:s3:::bucket-name/*"
             },
             {
                 "Effect": "Allow",
                 "Principal": "*",
                 "Action": "s3:ListBucket",
                 "Resource": "arn:aws:s3:::bucket-name"
             }
         ]
     }
     ```
   - enable static website hosting.
   - enable CORS, example:
     ```json
     [
         {
             "AllowedHeaders": [
                 "*"
             ],
             "AllowedMethods": [
                 "GET"
             ],
             "AllowedOrigins": [
                 "*"
             ],
             "ExposeHeaders": []
         }
     ]
     ```
4. **get a cert**: for https, because no one likes insecure websites.
5. **set up cloudfront**:
   - create a distribution with your cert.
   - enable http -> https upgrade.
   - set cache policy to `UseOriginCacheControlHeaders-QueryStrings`.
   - set origin request policy to `UserAgentRefererHeaders`.
   - if youre rich you can enable waf for ddos protection.
6. **point your domain**:
   - if using route 53: create an A record alias to the cloudfront domain.
   - otherwise: use a CNAME record.
7. **configure the site**:
   - edit `index.html` constants to match your use case.
7. **done!** now your pets are internet famous. 🎉

### 🎵 the track
it’s an ultra-compressed version of some kevin macleod(?) song. idk which one. it’s royalty-free, so no one’s coming after you.

### ⚠️ disclaimer
i don’t care what you do with this code. host your pet pics, host your memes, host your grandma’s recipes.
