import Image from 'next/image'
import Link from 'next/link'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Sigma } from 'lucide-react'
import MaxWidthWrapper from './MaxWidthWrapper'
import { User } from 'lucide-react'

interface ResponseBoxProps {
  response: string
}

function ResponseBox({response}: ResponseBoxProps) {
  return (
    <div className='flex md:w-1/2 w-full py-4 border-b border-x border-gray-500'>
      <User/>
      <p className='overflow-hidden'>{response}</p>
    </div>
  )
}

export default function Home() {
  return (
    <MaxWidthWrapper>
      <main className="flex min-h-screen flex-col items-center justify-between py-12">
        <ResponseBox response='sdlfkgjbdfljkbxdfskbldsfjbkxdbksldbxckjvblkjsfgbkjcxdflbkjsflkbs;ldjfbjkdsfnbklsdfnbkjsdnblkjsdnfbkjsdnfbkljsnbklsd' />
        <div className='flex md:w-1/2 w-full gap-2'>
          <Input className='border-gray-500 bg-transparent'/>
          <Button className='bg-gray-500'>
            <Sigma size={24}/>
          </Button>
        </div>
      </main>
    </MaxWidthWrapper>
  )
}
