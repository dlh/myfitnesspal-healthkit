# MyFitnessPal-HealthKit

Import MyFitnessPal nutrition information into Apple HealthKit.

## How It Works

The problem: After allowing MyFitnessPal to write nutrition data to HealthKit
only newly logged food will be written. The previous entries are not synced
into HealthKit.

This program traverses your food diary, *edits* the last food entry in each
meal, and saves it. MyFitnessPal will consider the data to be *new*, and write
it to HealthKit.

**The entries in your food diary are not altered.**

## Requirements

* [Python](https://www.python.org)
* [Selenium](http://www.seleniumhq.org)
* [Chrome](https://www.google.com/chrome/) and
  [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
* An ad-blocker extension for Chrome. uBlock Origin is recommended.

  You will need the `.crx` file, which can be downloaded from [this
  website](http://chrome-extension-downloader.com) by searching for extension
  ID `cjpalhdlnbpafiamejdnhcphjbkeiagm`.

## Usage

1. On your iOS device, make sure you have allowed MyFitnessPal to write data to
   HealthKit.
2. Run `./myfitnesspal-healthkit.py`.
3. Switch to the browser that opened, and log in to your account.
4. The program will begin traversing your food diary.

   Do not scroll the browser window, because it may cause an error to be
   raised.
   
   You can switch to another application and allow `myfitnesspal-healthkit.py`
   and its Chrome process to run in the background.
5. After your entire food diary has been traversed, stop the
   `myfitnesspal-healthkit.py` program by using `Control-C`.
6. Open MyFitnessPal on your iOS device. You should see the network activity
   indicator spinning, as the app is downloading the *updates* to your food
   diary.

## License

Copyright (c) 2016 DLH. See LICENSE.txt for the MIT license.
