from Datacredito import Datacredito

datacredito = Datacredito()

accounts = datacredito.getAccounts('1', '1189213694', 'SANCHEZ')
print(accounts)