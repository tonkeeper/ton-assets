const TonWeb = require('tonweb');
const tonweb = new TonWeb({
  provider: new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC', {
    apiKey: 'const TonWeb = require('tonweb');
const tonweb = new TonWeb({
  provider: new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC', {
    apiKey: 'const TonWeb = require('tonweb');
const tonweb = new TonWeb({
  provider: new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC', {
    apiKey: 'cb73a5ec3cd8b87dfc1e2be4ca6ca2ce48ed0ba390714d1e2c42781d39dc438c'
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

deployJetton();'
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

deployJetton();'
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

deployJetton();
