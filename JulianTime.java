package me.tristyn.pointsofinterest;

public final class JulianTime {
    
    //Variables
    static long millennialJulianDate = 2451545;                                 //Days since 2000 January 01 12:00:00.0
    static long millennialEpochTime  = 946728000000L;                           //msec since 2000 January 01 12:00:00.0
    
    static byte FROM_WEEKDAY = 0;
    static byte FROM_WEEK    = 1;
    
    
    
    
    //Constructors
    private JulianTime(){}
    
    //To JulianDate
    static double getJulianDate(){return getJulianDate(System.currentTimeMillis());}
    static double getJulianDate(long theTime){                                             //Converts milliSecFromEpoch to Julian Dates
        return millennialJulianDate+(double)(theTime-millennialEpochTime)/(86400000);   //Julian Dates are in TAI
        }
    static double getJulianDate(float year, float month, float day){               //Formula Found Online, Citation Needed.
        double a=Math.floor((14-month)/12);
        double y=year+4800-a;
        double m=month+12*a-3;
        return day+Math.floor((153*m+2)/(5))+365*y+Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)-32045;
        }
    static double getJulianDate(float year, float month, float day, float hour, float min, float sec){
        return getJulianDate(year,month,day) + HourMinToDayFraction(hour,min,sec);
        }
    
    static double getNextJulianDate(double julianDate, int myInt, byte id){
        if(      id==FROM_WEEKDAY ){return getNextJulianDateFromWeekday(julianDate,myInt);}
        //else if( id == FROM_WEEK  ){return getNextJulianDateFromWeekNumber(julianDate,myInt);}
        else{return 0;}
        }
    private static double getNextJulianDateFromWeekday(double julianDate, int dayOfWeek){
        // ToDo round to start of day.
        //julianDate-Math.floor(julianDate)
        int currentDayOfWeek = getDayOfWeek(julianDate);
        if( dayOfWeek >= 0 && dayOfWeek<=6 ) {
            while (dayOfWeek != currentDayOfWeek) {
                currentDayOfWeek++;
                julianDate++;
                if (currentDayOfWeek == 7){currentDayOfWeek = 0;}
                }
            return julianDate;
            }
        else{return julianDate;}
        }
   // private static double getNextJulianDateFromWeekNumber(double julianDate, int weekOfYear){}
        
    static double HourMinToDayFraction(float hour, float min, float sec){
        return (double)hour/24 + (double)min/1440 + (double)sec/86400;
        }
    static double HourMinToDayFraction(float hour, float min){
        return HourMinToDayFraction(hour,min,0);
        }
    
    //From JulianDate
    static long getEpochTime(double JulianDate){return (long)((JulianDate-millennialJulianDate)*86400000+millennialEpochTime);}
    static int  getDayOfWeek(double JulianDate){                                    //0 = Monday; 6=Sunday.
        double JD=JulianDate+.5;
        return (int)Math.floor(JD%7);
        }
    static int  getWeekNum(double julianDate){                                      //Formula Found Online, Citation Needed.
        int OD = getOrdinalDate(julianDate);
        int dow = getDayOfWeek(julianDate)+1;
        int WN = (int)Math.floor(((double)(OD-dow+10))/7);
        if(WN==53 || WN==1){
            int ThursdayOD=0;
            switch(dow){
                case 1:{ThursdayOD = JulianTime.getOrdinalDate(julianDate+3);break;}
                case 2:{ThursdayOD = JulianTime.getOrdinalDate(julianDate+2);break;}
                case 3:{ThursdayOD = JulianTime.getOrdinalDate(julianDate+1);break;}
                case 4:{ThursdayOD = JulianTime.getOrdinalDate(julianDate);break;}
                case 5:{ThursdayOD = JulianTime.getOrdinalDate(julianDate-1);break;}
                case 6:{ThursdayOD = JulianTime.getOrdinalDate(julianDate-2);break;}
                case 7:{ThursdayOD = JulianTime.getOrdinalDate(julianDate-3);break;}
                }
            WN=(int)Math.floor(((double)(ThursdayOD+6))/7);
            }
        return WN;
        }
    static int  getOrdinalDate(double JulianDate){                                      //Day of The Year (Formula Found Online, Citation Needed.)
        double StartOnGegDay = JulianDate-(millennialJulianDate-0.5);               //Days since 2000 January 01 00:00:00.0
        double wholeDays = Math.floor(StartOnGegDay);
        double y = Math.floor(StartOnGegDay/365.25);                                //Years since 2000
        double leapDays = Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)+1;    //+1 for 2000, but also counts current year
        boolean isleapYear=(y%4==0 && !(y%100==0)) || y%400==0;
        if(isleapYear){leapDays--;}
        //LeapDays is now number of leap days since 2000
        double yInDays = y*365+leapDays;                                            //Days since 2000,01,01,00,00,00
        double OrdinalYesterday = wholeDays-yInDays;
        return (int)OrdinalYesterday+1;
        }
    static int[] getGregorianTime(double JulianDate){                               //Formula Found Online, Citation Needed.
        double StartOnGegDay = JulianDate-(millennialJulianDate-0.5);               //Days since 2000 January 01 00:00:00.0
        double wholeDays = Math.floor(StartOnGegDay);
        double dayFraction = StartOnGegDay - wholeDays;
        
        double y=Math.floor(StartOnGegDay/365.25);                                  //Years since 2000
        double leapDays = Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)+1;    //+1 for 2000, but also counts current year
        boolean isleapYear=(y%4==0 && !(y%100==0)) || y%400==0;
        if(isleapYear){leapDays--;}
        //LeapDays is now number of leap days since 2000
        double yInDays = y*365+leapDays;                                            //Days since 2000,01,01,00,00,00
        double OrdinalYesterday = wholeDays-yInDays;
        double year=y+2000;
        
        int[] aa = {31,28,31,30,31,30,31,31,30,31,30,31};
        int month = 1;
        double days = OrdinalYesterday+1;
        for(int i:aa){
            if(days>i){month++;days=days-i;}
            if(isleapYear && i==28){days--;}
            }
        int[] HourMin = dayFractionToHourMin(dayFraction);
        int[] gregDate = {(int)year,(int)month,(int)days,HourMin[0],HourMin[1],HourMin[2]};
        return gregDate;
        }
    static int[] dayFractionToHourMin(double time){
        while(time >= 1){time -= 1;} while(time < 0){time += 1;}
        int Hour = (int)Math.floor(time*24);
        int Min = (int)Math.floor((time*24-Hour)*60);
        int Sec = (int)Math.floor(((time*24-Hour)*60-Min)*60);
        int[] TheTime = {Hour,Min,Sec};
        return TheTime;
        }
    
    //Astronomical
    static double moonAge(double JulianDate){
        return((JulianDate-(millennialJulianDate-0.5))-5.597661)/29.5305888610; //Age of Moon
        }
    static double meanSolarTime(float longitudeDeg,double JulianDate){
        double TerrestrialTimeCorrection = (32.184+10+27)/86400;                //Up-to-date as of December 2016
        //Terrestrial Time (TT) to Atomic Time (TAI) Correction.
        //32.184 seconds for historical difference
        //Leap seconds 10 seconds at the start of 1972, ic_plus the rest.
        double meanSolarTime = (longitudeDeg/360)+JulianDate-millennialJulianDate+TerrestrialTimeCorrection;
        return meanSolarTime;
        }
    static int[] sunrise(float Latitude, float Longitude){
        int[] riseSetHourMin = sunTimes(Latitude,Longitude);
        int[] riseHourMin= {riseSetHourMin[0],riseSetHourMin[1]};
        return riseHourMin;
        }
    static int[] sunset(float Latitude, float Longitude){
        int[] riseSetHourMin = sunTimes(Latitude,Longitude);
        int[] riseHourMin= {riseSetHourMin[2],riseSetHourMin[3]};
        return riseHourMin;
        }
    static int[] sunTimes(float Latitude, float Longitude){
        //From: http://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html
        //I don't understand, and it doesn't explain.
        double julianCentury = (getJulianDate()-millennialJulianDate)/36525;
        double geomMeanLongSun = (280.46646+julianCentury*(36000.76983 + julianCentury*0.0003032))%360;
        double geomMeanAnomalySun = 357.52911+julianCentury*(35999.05029 - 0.0001537*julianCentury);
        double eccentEarthOrbit = 0.016708634-julianCentury*(0.000042037+0.0000001267*julianCentury);
        double sunEqOfCtr = Math.sin(Math.toRadians(geomMeanAnomalySun))*(1.914602-julianCentury*(0.004817+0.000014*julianCentury))+Math.sin(Math.toRadians(2*geomMeanAnomalySun))*(0.019993-0.000101*julianCentury)+Math.sin(Math.toRadians(3*geomMeanAnomalySun))*0.000289;
        double sunTrueLong = geomMeanLongSun + sunEqOfCtr;
        double sunAppLong = sunTrueLong-0.00569-0.00478*Math.sin(Math.toRadians(125.04-1934.136*julianCentury));
        double meanObliqEcliptic = 23+(26+((21.448-julianCentury*(46.815+julianCentury*(0.00059-julianCentury*0.001813))))/60)/60;
        double obliqCorr = meanObliqEcliptic+0.00256*Math.cos(Math.toRadians(125.04-1934.136*julianCentury));
        double sunDeclin =Math.toDegrees(Math.asin(Math.sin(Math.toRadians(obliqCorr))*Math.sin(Math.toRadians(sunAppLong))));
        double y =Math.tan(Math.toRadians(obliqCorr/2))*Math.tan(Math.toRadians(obliqCorr/2));
        double eqOfTime =4*Math.toDegrees(y*Math.sin(2*Math.toRadians(geomMeanLongSun))-2*eccentEarthOrbit*Math.sin(Math.toRadians(geomMeanAnomalySun))+4*eccentEarthOrbit*y*Math.sin(Math.toRadians(geomMeanAnomalySun))*Math.cos(2*Math.toRadians(geomMeanLongSun))-0.5*y*y*Math.sin(4*Math.toRadians(geomMeanLongSun))-1.25*eccentEarthOrbit*eccentEarthOrbit*Math.sin(2*Math.toRadians(geomMeanAnomalySun)));
        double HASunrise = Math.toDegrees(Math.acos(Math.cos(Math.toRadians(90.833))/(Math.cos(Math.toRadians(Latitude))*Math.cos(Math.toRadians(sunDeclin)))-Math.tan(Math.toRadians(Latitude))*Math.tan(Math.toRadians(sunDeclin)))); //Possibly in Min
        double solarNoon = (720-4*Longitude-eqOfTime)/1440;
        double sunriseTime = solarNoon-HASunrise*4/1440;
        double sunsetTime = solarNoon+HASunrise*4/1440;
        //Convert to Hour Min
        int[] sunrise = dayFractionToHourMin(sunriseTime);
        int[] sunset = dayFractionToHourMin(sunsetTime);
        int[] riseSetHourMin = {sunrise[0],sunrise[1], sunset[0],sunset[1]};
        return riseSetHourMin;
        }
    
    }
