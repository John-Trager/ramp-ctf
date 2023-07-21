# Ramp CTF

Taken July 20th 2023.

Ramp has a CTF they used for applications as opposed to a leetcode style OA.

Here is my writeup of my experience solving the challenge.

## Intro
The challenge begins by taking you to a url: [https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/](https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/)

We first see a string that appears to be gibberish but upon looking closer we find that it is in fact [base64 encoded string](https://en.wikipedia.org/wiki/Base64). We can decrypt using a simple online website [base64decode](https://www.base64decode.org/).

The message says some things about the challenge but most importantly that the flags are 7 character long strings (that can be found in a dictionary) and that we need at least 2 (they also don't specify on how many there are but supposedly only 4?).

Next what we need to realize is that the url has something interesting going on :

```
https://.../dev/start?q=select%20contents%20from%20readme
```

Now if we look closely we can see that this looks just like SQL straight in the URL `SELECT contents FROM readme`! The next obvious move is to look around and see what tables are in the SQL database by injecting our own SQL commands into the url. If we mess around with the commands we can see we get an error message `"SQLite error"` telling us that the SQL database is SQLite. We can then find what tables are in the database with:

```SQL
SELECT name FROM sqlite_master
```

or in the url form:

```
https://.../dev/start?q=select%20name%20from%20sqlite_master
```

We then find something like `[["readme"], ["flags_xxx"]]`. We already have seen the contents of the readme but we should now checkout what is in this flags table. But first we need to understand that we don't know what columns are in the table so how will we know what data we can query? Fortunately we can look at the columns in the table by using the command:

```SQL
PRAGMA table_info(flags_xxx)
```

again out into the url:

```
https://.../dev/start?q=PRAGMA%20table_info(flags_xxx)
```

We get the resulting columns to be ` [[0, "url", "text", 0, null, 0]]`. I am still unsure what the 0 and null is but we can explore the data in `url` and `text`.

```SQL
SELECT url FROM flags_xxx
```

```
https://.../dev/start?q=select%20url%20from%20flags_xxx
```

We find `[["/browser"], ["/hash"], ["/exception"], ["/stream"]]`. By doing some thinking we can figure out that these are alternative urls that we can access (and they end up being the 4 different challenges that I could find).

I am still not sure if there is other information we can find in the flags_xxx table. Perhaps there is something to do with `text` but when I ran the query it always gave me errors. If there are more flags to be found though I would reckon they are somewhere here.

## 4 challenges

We can access the challenges by going to their URLs like:

```
https://.../dev/browser
```

### /browser
The browser challenge greets is with:

```
File \"/var/task/app.py\", line 258, in get\n    raise InvalidUserAgent(expected_user_agent)\nMozilla/8.8 (Macintosh; Intel Mac OS X 8888_8888) AppleWebKit/888.8.88 (KHTML, like Gecko) Version/88.8.8 Safari/888.8.88
```

What we can see from this is that some app.py is being run and checking our browsers user agent. It expected a particular user agent specifically `Mozilla/8.8 (Macintosh...` and our browser is not that agent. 

We can then simply spoof our browser agent by putting in the expected user agent into our GET request. This can be found in the [browser_spoof.py](browser_spoof.py)

### /hash
The hash challenge greets is with:

```
md5(flag+salt):7203a7a12aea1ba959c28aa88ca6598b:416ae287f634
```

Note here that `7203a7a12aea1ba959c28aa88ca6598b` is the encrypted value and `416ae287f634` is the salt.

We can see that this is some kind of encryption and in this case it is [md5](https://en.wikipedia.org/wiki/MD5). We can also see that it has provided us with the encrypted flag (supposedly) and the "salt". 

We can think of the salt in this case like the seed of the encryption. Encryption functions by there nature are 1 direction. Once we encrypt the value we can't decrypt it. But in the case with md5 and knowing the salt (or "random seed") we can reproduce the encrypted hashes and find our flag by brute-force. 

To brute-force solve for the flag we need to recall that the flag is a 7 character dictionary word. Thus what we can do is get a list of [7 character long words](data/word-list-7-letters.txt) hash them using md5 and the provided salt and see if the encrypted value matches with the provided encrypted value. [hash_md5.py](hash_md5.py) was used to implement the brute-force method and solve the flage.

### /exception
The hash challenge greets is with:
```
"  File \"/var/task/app.py\", line 322, in get\n    raise StartsWithH\n"
```

This can be a little confusing at first until you look at the URL:
```
https://.../dev/exception?q=hello
```

From this we can see that "hello" was the value input to the program and that it was the incorrect as it shouldn't start with "H". We can then try out some other words or letters and find that there are some other constraints as well:

- Doesn't start with "H"
- No "L"s in the word
- ASCII values of the string add to 42
- ~7 characters long (inferred by testing out different lengths and also the hint that the key is 7 letters long)
    - I should not that it could likely be longer

There are likely other constraints but with this information I created a program to solve for the correct key. I found a list of dictionary words that [ASCII values add up to 42](data/word-42-list.txt) which was found [here](https://gist.github.com/stripthis/5430226). I then went though the list and eliminated words that violated the constraints. I found many answers but "peached" was the one I went with to get the key (to be clear "peached" was not the actual flag). The flag was then displayed when I put in this value.

### /stream
The stream challenge greets is with:

```
"u"
```

Then we can run it again and see that it gives us a different character but also repeats. From this I decided to go the route of sampling a bunch of times what the characters were ([stream_sample.py](stream_sample.py)). I then took this list of unique characters and found words that contained all of the characters and were 7 letters long ([stream_lookup.py](stream_lookup.py)). This resulted in only having a single answer which I assumed was the flag. You can also use a website like [word finder](https://word.tips/) to find words that contain the characters.


## Conclusion

The CTF was pretty interesting and exposed me to some new topics that I had't seen before. Ultimately if you're seeing this I didn't get the job but still a productive and fun night spent solving it.

Hopefully I can solve some more CTFs in the future and maybe find other flags in this challenge.