<!--next-version-placeholder-->

## v0.5.0 (2023-01-03)
### Feature
* Add helper method to check whether function is tracked :droplet: ([`759cb93`](https://github.com/bmwant/spoor/commit/759cb931bedafa327b372bf289d1a901a76910b0))
* Add flag to allow tracking dunder methods :clock6: ([`fb5d4c2`](https://github.com/bmwant/spoor/commit/fb5d4c21530de955bc6460e66d1216fb11f00c43))
* Add rich protocol to func call dataclass :information_source: ([`e4b374d`](https://github.com/bmwant/spoor/commit/e4b374d16e0f2c4125344adf32cafafd06a44842))
* Allow to access function call via dictionary syntax :kissing_cat: ([`40ccf3e`](https://github.com/bmwant/spoor/commit/40ccf3ebecd68c1ece40b4c0a79a1e3864e3eca7))
* Decorate both functions and methods with a same class :city_sunrise: ([`36418c3`](https://github.com/bmwant/spoor/commit/36418c3f02c006f33e0293f86a901d546096b936))
* Activate attach feature for functions tracking :kr: ([`b1618b2`](https://github.com/bmwant/spoor/commit/b1618b25da2ad9aa7231e11ed277c3373b313157))
* Implement attach for functions tracking :curly_loop: ([`167ead1`](https://github.com/bmwant/spoor/commit/167ead1d13bc1148164428bdd1757e5700666a56))
* Add logging to the package :mag: ([`7956678`](https://github.com/bmwant/spoor/commit/7956678bd0b7706b29ddb72ed4de5cb64e69b089))
* Add statsd exporter implementation :mobile_phone_off: ([`495d548`](https://github.com/bmwant/spoor/commit/495d548e064b1c0a5a5f99e2b27f722e4b060312))

### Fix
* Control highlight for func call rich objects :koko: ([`dbe1be0`](https://github.com/bmwant/spoor/commit/dbe1be09045d335e4d21cc87ebdfadd84fd8877d))
* Make func a private attribute :rice_scene: ([`581c3cb`](https://github.com/bmwant/spoor/commit/581c3cbf1aafb78bdce026eef1958da4f3bbee52))

### Documentation
* Testing examples :rage3: ([`3b50cdf`](https://github.com/bmwant/spoor/commit/3b50cdf58473794b97369bf2d46a982210c226bb))
* Add example to track class :moyai: ([`a061a09`](https://github.com/bmwant/spoor/commit/a061a09a00b3eed04a793da13b38e57f56fd3f6a))
* Add example to track functions :pouch: ([`9445fee`](https://github.com/bmwant/spoor/commit/9445feefa9fd1961b17e9d48836eabbb0b2dcbc5))

## v0.4.0 (2022-12-28)
### Feature
* Exporter sends same metric with tags attached :baby_bottle: ([`8fdc5db`](https://github.com/bmwant/spoor/commit/8fdc5dbb1f7b90d9c66142c4650f7c53217778c6))

## v0.3.4 (2022-12-28)
### Fix
* Do not remove dist directory on publish :frog: ([`1ba92d0`](https://github.com/bmwant/spoor/commit/1ba92d05ff3dfff7fef612ccd5de11d35500f47c))

### Documentation
* Update readme with config options :vs: ([`dc2de3e`](https://github.com/bmwant/spoor/commit/dc2de3eac207f6c1c6e88dfe1ffb308a9929990c))

## v0.3.3 (2022-12-28)
### Fix
* Upload package to PyPI on release creation :monkey_face: ([`f0f4dde`](https://github.com/bmwant/spoor/commit/f0f4dde2cb8b0f00322950097fbcf0c768cb86a5))

## v0.3.1 (2022-12-27)
### Fix
* Attach artifact to github release :cool: ([`f961d39`](https://github.com/bmwant/spoor/commit/f961d3901672ee4dd0d64464acd8ebe4e5e84dc5))

### Documentation
* Update readme with extra links :telephone: ([`0ff612a`](https://github.com/bmwant/spoor/commit/0ff612a4e055ee4b6df0f523099a2fa7308151e2))

## v0.3.0 (2022-12-27)
### Feature
* Flush all data to exporters on garbage collections :mailbox_with_mail: ([`75cd2dc`](https://github.com/bmwant/spoor/commit/75cd2dc58e2cba6a14595ce3b89b067bef20bc2d))
* Add datadog exporter :airplane: ([`d4d2b8c`](https://github.com/bmwant/spoor/commit/d4d2b8c565316c24854e318cae6c015326ec0cea))
* Add rich protocol to topn statistics table :oncoming_automobile: ([`ac7da94`](https://github.com/bmwant/spoor/commit/ac7da94459e779e695eb15c2a7a5d8b0b0a87281))
* Add topn methods for most called functions :sushi: ([`bf1b393`](https://github.com/bmwant/spoor/commit/bf1b39309bc3bf9bc947ab0bde0b9c05d56cbf69))
* Add rich to pretty output call statistics :open_file_folder: ([`54aefd9`](https://github.com/bmwant/spoor/commit/54aefd97e1ac2889cffb3e4819ec412cc3eead79))
* Add ability to track invocations across different instances :earth_asia: ([`d67a83f`](https://github.com/bmwant/spoor/commit/d67a83fddf0d6e613efb314ba23cccac40d05f3b))
* Allow enabling and disabling tracking :high_heel: ([`df5e5ea`](https://github.com/bmwant/spoor/commit/df5e5ea007d741ac6fc3b82363e61110169c70d5))
* Do not track dunder methods on classes :older_man: ([`9038cb3`](https://github.com/bmwant/spoor/commit/9038cb3b17a5c45f33ce10f018bdd59bb1d48f25))
* Implement tracking methods :stuck_out_tongue: ([`0d8937e`](https://github.com/bmwant/spoor/commit/0d8937ea7ff65ee7a21f911735426292f0535400))

### Fix
* Make type hints work with python 3.8 :clock3: ([`1ec47b4`](https://github.com/bmwant/spoor/commit/1ec47b40236aa6637f4520454ea3bc3ead059d9b))
* Allow tracking same method on different instances as one :dvd: ([`583a16e`](https://github.com/bmwant/spoor/commit/583a16ec8c6b2f4944f3867267db1d4cd4d1d196))

### Documentation
* Testing tables :tokyo_tower: ([`e6104ab`](https://github.com/bmwant/spoor/commit/e6104abf654374082e8487d64f53484f06964ef4))
* Update readme :clock11: ([`0ae4b18`](https://github.com/bmwant/spoor/commit/0ae4b1853ae3d35a4bd1eb8cd08659b5aa8fd8f1))
