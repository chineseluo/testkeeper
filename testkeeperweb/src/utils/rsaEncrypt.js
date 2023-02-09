import JSEncrypt from 'jsencrypt/bin/jsencrypt.min'

// 密钥对生成 http://web.chacuo.net/netrsakeypair

const publicKey = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANnc1KIw8N+feeDJbVRNGg1PF3VCfLPO\n' +
  '1Ebkl9zJzYoRfDlOAKMgHurZuRA0AdK+jQAMu9z76jpZnqlOfFgew5UCAwEAAQ=='

// 加密
export function encrypt(txt) {
  const encryptor = new JSEncrypt()
  encryptor.setPublicKey(publicKey) // 设置公钥
  return encryptor.encrypt(txt) // 对需要加密的数据进行加密
}

