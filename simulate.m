T=16;
File=load('input.txt');
num_wall=File(1:1,1:1);
num_ap=File(1:1,2:2);
walls=File(2:1+2*num_wall,:);
aps=File(2+2*num_wall:1+2*num_wall+num_ap,:);
mp=File(2+2*num_wall+num_ap:2+2*num_wall+num_ap,:);
num=zeros(1,num_ap);
for i=1:num_ap
    answer=[];
    n=0;
    for j=1:num_wall
        if mp(1,1)==aps(i,1) && walls(2*j-1,1)==walls(2*j,1)
            if walls(2*j-1,2)>=walls(2*j,2)
                maxyw=walls(2*j-1,2);
                minyw=walls(2*j,2);
            else
                minyw=walls(2*j-1,2);
                maxyw=walls(2*j,2);
            end
            if mp(1,2)>=aps(i,2)
                maxyma=mp(1,2);
                minyma=aps(i,2);
            else
                minyma=mp(1,2);
                maxyma=aps(i,2);
            end
            if mp(1,1)==walls(2*j-1,1) && minyma<=minyw && maxyma>=maxyw
                num(1,i)=num(1,i)+1;
            end
            continue;
        end
        if mp(1,1)==aps(i,1)
            if walls(2*j-1,1)>=walls(2*j,1)
                minx=walls(2*j,1);
                maxx=walls(2*j-1,1);
            else
                maxx=walls(2*j,1);
                minx=walls(2*j-1,1);
            end
            if mp(1,1)>maxx || mp(1,1)<minx
                continue;
            end
            k=(walls(2*j,2)-walls(2*j-1,2))/(walls(2*j,1)-walls(2*j-1,1));
            b=walls(2*j,2)-k*walls(2*j,1); 
            y=k*mp(1,1)+b;
            if aps(i,2)>=mp(1,2)
                miny=mp(1,2);
                maxy=aps(i,2);
            else
                maxy=mp(1,2);
                miny=aps(i,2);
            end
            if y<=maxy && y>=miny
                sig=0;
                for a=1:n
                    if answer(a,1)==mp(1,1) && answer(a,2)==y
                        sig=1;
                        break;
                    end
                end
                if sig==0
                    answer=[answer;mp(1,1) y];
                    n=n+1;
                end
            end
        end
        if walls(2*j-1,1)==walls(2*j,1)
            if mp(1,1)>=aps(i,1)
                minx=aps(i,1);
                maxx=mp(1,1);
            else
                maxx=aps(i,1);
                minx=mp(1,1);
            end
            if walls(2*j-1,1)>maxx || walls(2*j-1,1)<minx
                continue;
            end
            k=(mp(1,2)-aps(i,2))/(mp(1,1)-aps(i,1));
            b=mp(1,2)-k*mp(1,1); 
            y=k*walls(2*j-1,1)+b;
            if walls(2*j-1,2)>=walls(2*j,2)
                miny=walls(2*j,2);
                maxy=walls(2*j-1,2);
            else
                maxy=walls(2*j,2);
                miny=walls(2*j-1,2);
            end
            if y<=maxy && y>=miny
                sig=0;
                for a=1:n
                    if answer(a,1)==walls(2*j-1,1) && answer(a,2)==y
                        sig=1;
                        break;
                    end
                end
                if sig==0
                    answer=[answer;walls(2*j-1,1) y];
                    n=n+1;
                end
            end
            continue;
        end
        if mp(1,1)~=aps(i,1) && walls(2*j-1,1)~=walls(2*j,1)
            k1=(walls(2*j,2)-walls(2*j-1,2))/(walls(2*j,1)-walls(2*j-1,1));
            k2=(mp(1,2)-aps(i,2))/(mp(1,1)-aps(i,1));
            b1=walls(2*j,2)-k1*walls(2*j,1);
            b2=mp(1,2)-k2*mp(1,1);
            if k1==k2
                if b1==b2
                    num(1,i)=num(1,i)+1;
                end
            else
                x=(b2-b1)/(k1-k2);
                if walls(2*j-1,1)>=walls(2*j,1)
                    minx1=walls(2*j,1);
                    maxx1=walls(2*j-1,1);
                else
                    maxx1=walls(2*j,1);
                    minx1=walls(2*j-1,1);
                end
                if aps(i,1)>=mp(1,1)
                    minx2=mp(1,1);
                    maxx2=aps(i,1);
                else
                    maxx2=mp(1,1);
                    minx2=aps(i,1);
                end
                if x>=minx1 && x<=maxx1 && x>=minx2 && x<=maxx2
                    y=k1*x+b1;
                    sig=0;
                    for a=1:n
                        if answer(a,1)==x && answer(a,2)==y
                            sig=1;
                            break;
                        end
                    end
                    if sig==0
                        answer=[answer;x y];
                        n=n+1;
                    end
                end
            end
        end
    end
    num(1,i)=num(1,i)+n;
end
dist_ap=zeros(1,num_ap);
time_ap=zeros(1,num_ap);
ssi_ap=zeros(1,num_ap);
c=clock();
n1=datenum(datestr(now,1));
n2=datenum('01-Jan-1970');
time=1000*((n1-n2)*24*3600+c(4)*3600+c(5)*60+c(6));
for i=1:num_ap
    time_ap(1,i)=time+fix(T*rand(1,1));
    dist_ap(1,i)=norm(aps(i:i,:)-mp(1:1,:));
    ssi_ap(1,i)=-30-10*3*log10(dist_ap(1,i))+1/sqrt(2*pi*4)*exp((-dist_ap(1,i)*dist_ap(1,i)))-5*num(1,i);
end
filename = 'sql.txt';
fid = fopen(filename, 'w');
fprintf(fid, 'INSERT INTO trainer_postion VALUES(1,00-00-00-00-00-00,%d,0,0)\n',time);
id=2;
for i=1:num_ap
    fprintf(fid,'INSERT INTO trainer_device VALUES(%d,00-00-00-00-00-00,%f,%d,%d)\n',id,ssi_ap(1,i),time_ap(1,i),i);
    id=id+1;
end
