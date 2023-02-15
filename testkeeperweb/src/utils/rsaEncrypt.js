import JSEncrypt from 'jsencrypt/bin/jsencrypt.min'

// 密钥对生成 http://web.chacuo.net/netrsakeypair

const publicKey = '-----BEGIN PUBLIC KEY-----\n' +
  'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMuRh08n07eFElnLUTRo/ZIGI548BP3wNVYlfNJEJD0dRKD/9Gkc38R0daDrdtGbnck1WtQaVwNwQViMXL//bZMCAwEAAQ==\n' +
  '-----END PUBLIC KEY-----'

// 加密
export function encrypt(txt) {
  const encryptor = new JSEncrypt()
  encryptor.setPublicKey(publicKey) // 设置公钥
  return encryptor.encrypt(txt) // 对需要加密的数据进行加密
}

