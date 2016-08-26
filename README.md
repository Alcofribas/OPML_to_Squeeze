# OPML_to_Squeeze
_Update Podcast Subscription in Squeezebox App From OPML File Automatically_

## Background

My first encounter with music streaming in 2010 was a [Logitech Squeezebox Duet](http://support.logitech.com/en_us/product/squeezebox-duet). Today, I still use it occasionally as a convenient option to listen to internet radio or podcasts at home. However, convenience ends in the case of the Squeezebox when it comes to managing your podcast subscriptions. For this, you usually cannot avoid using the web interface on http://www.mysqueezebox.com which dosn't provide an OPML import option. Therefore, adding and deleting podcasts in the Squeezebox App is a painful process.  

As I mainly use my mobile for dealing with podcasts, I created this script to easily update the subscription list within the Squeezebox with a bot based on PhantomJS using an OPML file containing the current subscription list exported from my mobile podcatcher. 

## Prerequisites

- Python 2.7  
- Python libraries: Selenium, Listparser  
- PhantomJS  

## Usage

You have to  
1. fill in your credentials for http://www.mysqueezebox.com within the script  
2. set the correct filename  
3. run the script…  

## Caveats

Currently the mysqueezebox subscription list is deleted without being backed up, so make sure you're OK with that before running the script. 

## Feedback

If you find this script useful or have any comments or suggestions, your feedback is much appreciated.  
