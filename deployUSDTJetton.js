const TonWeb = require('tonweb');
const tonweb = new TonWeb({
  provider: new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC', {
    apiKey: '2c8c14a671564cd1a6f2244796c967b39fc25cb29fc9f53147546d86cbfd1167'
  })
});

async function deployJetton() {
  try {
    const deploymentResult = await tonweb.provider.send('deployJettonMaster', {
      adminAddress: '0:FA146529B8E269FFCD7A5EACF9473B641E35389C302D7E8C3DF56EB3DE9C7F01',
      totalSupply: '1000000000000000000',
      mintable: false,
      decimals: 6,
      name: 'Tether USD',
      symbol: 'USD'
    });
    console.log('Jetton deployed successfully:', deploymentResult);
  } catch (error) {
    console.error('Error deploying jetton:', error);
  }
}

deployUSDTJetton();
