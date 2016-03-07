import pingpp

class PayProcess:
	app_key = 'sk_test_Oyj9a5enfDa9W1WLu9i1CyDK'
	#app_key = 'sk_live_rLS4CSOeT0uPmvHGa58e584K'
	appid = 'app_y9ujPCq9WbrDn50y' 
	@staticmethod
	def get_charge(order_no, channel, amount, client_ip, subject,body):
		pingpp.api_key = PayProcess.app_key
		ch = pingpp.Charge.create(
				order_no=order_no,
				amount=amount,
				app=dict(id=PayProcess.appid),
				channel=channel,
				currency='cny',
				client_ip=client_ip,
				subject=subject,
				body=body,
				)
		print ch
		return ch

