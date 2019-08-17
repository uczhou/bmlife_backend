## BMLIFE Backend
### Description
This project is an amateur project. The frontend is [iOS app](https://github.com/zijiazhai/BMLF), which can be downloaded from App Store by searching 'bmlife'.

The crime data is downloaded from public database. Total crime data is around <strong>15G</strong> and more than <strong>100 M lines</strong>.

The backend project implements the following functions:
1. List House
2. Add House
3. List Houses in Closed Area
4. Get House by uuid
5. Modifiy House information
6. List crimes in Closed Area
7. List Zip Codes with boundary and Crimes Count in Closed Area
8. Get Zip Code boundary

### Technical details
1. Framework: Django REST Framework + django-rest-framework-gis
2. Database: Postgresql
3. Deploy environment: AWS EC2, AWS RDS

### Some Tips
1. Use large table instead of multiple tables connected with foreign keys to store House
At first version, we use multiple tables to store House object, but the searching speed is really slow. So in the second version, we refract the tables and aggregate those small tables into a single large table.
The searching speed increases dramatically.
 
2. Offline computation of Geo data
Geo data real time computation is slow and costs a lot of resources. So we computed the crime geo data offline and support retrieval of crime data in city level.


### APIs

##### 1. List Houses:
```buildoutcfg
Method: GET
Endpoint: /api/v1/rental/house/
```

##### 2. Add House:
```buildoutcfg
Method: POST
Data: 
Endpoint: /api/v1/rental/house/
```

##### 3. List Houses in Closed Area:
```buildoutcfg
Method: POST
Data: {"in_polygon": "20,60,22,60,22,65,20,65,20,60"}
Endpoint: /api/v1/rental/house/polygon/
```

##### 4. Get House by uuid:
```buildoutcfg
Method: GET
Endpoint: /api/v1/rental/house/<uuid>
Example: /api/v1/rental/house/4929b65d-28da-4e94-afd7-aee8cb2047ab

```

#### 5. Modify House:
```buildoutcfg
Method: PUT
Data: same as add
Endpoint: /api/v1/rental/house/<id>
Example: /api/v1/rental/house/1
```

#### 6. List crimes in state
```buildoutcfg
Method: GET
Required: <state>
Endpoint: /api/v1/info/crime/<state>/
Example: /api/v1/info/crime/il/

```

##### 7. List Crimes in Closed Area:
```buildoutcfg
Method: POST
Required: <state>
Data: {"in_polygon": "20,60,22,60,22,65,20,65,20,60"}
Endpoint: /api/v1/info/crime/<state>/
Example: /api/v1/info/crime/il/

```

##### 8. List Zip Codes with boundary and Crimes Count in Closed Area:
```buildoutcfg
Method: POST
Required: <state>
Data: {"in_polygon": "20,60,22,60,22,65,20,65,20,60"}
Endpoint: /api/v1/location/zipcode/areas/
Example: /api/v1/location/zipcode/areas/

```

##### 9. Get Zip Code boundary:
```buildoutcfg
Method: GET
Endpoint: /api/v1/location/zipcode/<zipcode>
Example: /api/v1/location/zipcode/60611

```
