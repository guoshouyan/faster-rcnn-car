function rec = VOCreadxml(path)

if length(path)>5&&strcmp(path(1:5),'http:')
    xml=urlread(path)';
else
    f=fopen(path,'r');
    xml=fread(f,'*char')';
    xml=xml(1,23:end);
    fclose(f);
end
rec=VOCxml2struct(xml);
