syntax="proto3";
package measure;

message Tag{
    string key =1;
    string value =2;
}

message IntField{
    string key =1;
    int32 value =2;
}

message FloatField{
    string key =1;
    float value =2;
}

message MeasurePayload{
    repeated Tag tags = 1;
    repeated IntField intFields = 2;
    repeated FloatField floatFields = 3;
}

