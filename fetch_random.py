import requests
for number in range(400,800):
    r = requests.get('http://lorempixel.com/400/400/')
    if r.status_code == 200:
        with open("images/%04d.jpg" % number,'w') as fh:
            fh.write(r.content)
            print("fetched image %d" % number)

