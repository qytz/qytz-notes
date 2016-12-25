#!/usr/bin/python

def get_flower(n, ofile):
  D_pow=[pow(i,n) for i in range(0,10)]
  V_min=1*pow(10,n-1)
  V_max=sum((9*pow(10,x) for x in range(0,n)))
  T_count=0
  print D_pow, V_max, V_min
  nums=[1]+[0]*(n-1)
  print 'Start:', nums

  idx=n-1
  tmp_l=[0]*10
  while True:
    nums[idx]+=1
    if nums[idx]<10:
      j=idx+1
      while j<n:
        nums[j]=nums[idx] # reset
        j+=1
      v=sum((D_pow[x] for x in nums))
      if v<=V_max and v>=V_min:
        T_count+=1
        #test if is flower
        #print 'do test:', ''.join(map(str,nums))
        k=0
        while k<10:
          tmp_l[k]=0
          k+=1
        N=0
        for k in nums:
          tmp_l[k]+=1
          N+=1
        while N>0:
          p=v%10
          if tmp_l[p]>0:
            tmp_l[p]-=1
            N-=1
          else:
            break
          v/=10
        if N==0:
          print >>ofile, 'hit', sum((D_pow[x] for x in nums))
      idx=n-1
    elif idx==0:
      print 'done'
      break
    else:
      idx-=1
  print 't_count', T_count

if __name__ == '__main__':
  with file('./f.txt', 'wb') as o:
    get_flower(21, o)
    #get_flower(3, o)
