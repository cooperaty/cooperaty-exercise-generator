import { I } from 'ipfsio'

// Your api key from NFTStorage
const i = new I('api key from NFTStorage')



export async function store(path) {
    const cid = await i.file(path)
    // console.log(cid)
    return cid
}
