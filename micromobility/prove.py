from micromobility.tools import ethTestnet
from micromobility.models import Auction


a = Auction.objects.all()

data = a[2].dataSerializer()
net = ethTestnet(data)
print(net.transaction())

