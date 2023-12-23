import mraa
import cgi
import cgitb

WAY = mraa.Gpio(43) #GPIO43 on 7688
WAY.dir(mraa.DIR_OUT)
cgitb.enable()
ip_addr = "http://172.20.10.3/"

if __name__ == "__main__":
  form = cgi.FieldStorage()       #Get the form instance
  DIRECT = form.getvalue('LED')   #Get the value from posted web form
  redirectURL = ip_addr+"controlGPIO.html"
  url_404 = ip_addr+"404page.html"

  if DIRECT == "U":               #Decide the LED is on or off
    #WAY.write(1)
    print 'Content-Type: text/html'
    print 'Location: %s' % redirectURL
    print # HTTP says you have to have a blank line between headers and content
    print '<html>'
    print '  <head>'
    print '    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL
    print '    <title>You are going to be redirected</title>'
    print '  </head>' 
    print '  <body>'
    print '    Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL
    print '  </body>'
    print '</html>'
  else:
    #WAY.write(0)
    print 'Content-Type: text/html'
    print 'Location: %s' % url_404
    print # HTTP says you have to have a blank line between headers and content
    print '<html>'
    print '  <head>'
    print '    <meta http-equiv="refresh" content="0;url=%s" />' % url_404
    print '    <title>You are going to be redirected</title>'
    print '  </head>' 
    print '  <body>'
    print '    Redirecting... <a href="%s">Click here if you are not redirected</a>' % url_404
    print '  </body>'
    print '</html>'