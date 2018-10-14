import smtplib
import itchat
import pickle

email_wechat_dict = pickle.load(open("records/email.txt", "rb"))

def sendEmail(userName):
	gmail_user = email_wechat_dict[userName][0] #From email
	gmail_pwd = email_wechat_dict[userName][1] #Login password
	TO = email_wechat_dict[userName][2] #To email
	SUBJECT = "SOS"
	TEXT = "Help!"
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	BODY = '\r\n'.join(['To: %s' % TO,
	        'From: %s' % gmail_user,
	        'Subject: %s' % SUBJECT,
	        '', TEXT])

	server.sendmail(gmail_user, [TO], BODY)
	print ('email sent')


def sendWechatMessage(userName):
	itchat.auto_login(hotReload=True)
	wechatFriend = email_wechat_dict[userName][3]
	friendName = unicode(wechatFriend, "utf-8")
	user = itchat.search_friends(name = friendName)
	UserName  = user[0]['UserName']
	itchat.send('SOS! Help!',toUserName=UserName)
	itchat.run()