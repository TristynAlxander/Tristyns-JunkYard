package xmlapp;

//Imports
import org.w3c.dom.*;
import javax.xml.validation.*;
    //import javax.xml.validation.Schema;
    //import javax.xml.validation.SchemaFactory;
    //import javax.xml.validation.Validator;
import javax.xml.transform.*;
    import javax.xml.transform.dom.DOMSource;
    import javax.xml.transform.stream.StreamResult;
    import javax.xml.transform.stream.StreamSource;

import javax.xml.parsers.*;
import javax.xml.XMLConstants;



import java.io.*;
import java.util.Arrays;

final class JulianTimeConverter{                                                //To Do: Add citations.
    //Variables
    static long millennialJulianDate = 2451545;                                 //Days since 2000 January 01 12:00:00.0
    static long millennialEpochTime = 946728000000L;                            //msec since 2000 January 01 12:00:00.0
    
    //Constructors
    private JulianTimeConverter(){}
    
    //To JulianDate
    static double JulianDate(){return JulianDate(System.currentTimeMillis());}
    static double JulianDate(long theTime){                                             //Converts milliSecFromEpoch to Julian Dates 
        return millennialJulianDate+(double)(theTime-millennialEpochTime)/(86400000);   //Julian Dates are in TAI
        }
    static double JulianDate(float year, float month, float day){               //Formula Found Online, Citation Needed.
        double a=Math.floor((14-month)/12); 
        double y=year+4800-a; 
        double m=month+12*a-3;
        return day+Math.floor((153*m+2)/(5))+365*y+Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)-32045;
        }
    static double JulianDate(float year, float month, float day, float hour, float min, float sec){
        return JulianDate(year,month,day) + HourMinToDayFraction(hour,min,sec);
        }
    static double HourMinToDayFraction(float hour, float min, float sec){
        return (double)hour/24 + (double)min/1440 + (double)sec/86400;
        }
    static double HourMinToDayFraction(float hour, float min){
        return HourMinToDayFraction(hour,min,0);
        }
    
    //From JulianDate
    static int DayOfWeek(double JulianDate){                                    //0 = Monday; 6=Sunday.
        double JD=JulianDate+.5;
        return (int)Math.floor(JD%7);
        }
    static int weekNum(double julianDate){                                      //Formula Found Online, Citation Needed.
            int OD = OrdinalDate(julianDate);
            int dow = DayOfWeek(julianDate)+1;
            int WN = (int)Math.floor(((double)(OD-dow+10))/7);
            if(WN==53 || WN==1){
                int ThursdayOD=0;
                switch(dow){
                    case 1:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate+3);break;}
                    case 2:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate+2);break;}
                    case 3:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate+1);break;}
                    case 4:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate);break;}
                    case 5:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate-1);break;}
                    case 6:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate-2);break;}
                    case 7:{ThursdayOD = JulianTimeConverter.OrdinalDate(julianDate-3);break;}
                    }
                WN=(int)Math.floor(((double)(ThursdayOD+6))/7);
                }
            return WN;
            }
    static int OrdinalDate(double JulianDate){                                      //Day of The Year (Formula Found Online, Citation Needed.)
        double StartOnGegDay = JulianDate-(millennialJulianDate-0.5);               //Days since 2000 January 01 00:00:00.0
        double wholeDays = Math.floor(StartOnGegDay);
        double y = Math.floor(StartOnGegDay/365.25);                                //Years since 2000
        double leapDays = Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)+1;    //+1 for 2000, but also counts current year
        boolean isleapYear=(y%4==0 && !(y%100==0)) || y%400==0;
        if(isleapYear){leapDays--;}
        //LeapDays is now number of leap days since 2000
        double yInDays = y*365+leapDays;                                            //Days since 2000,01,01,00,00,00
        double OrdinalYesterday = wholeDays-yInDays;
        return (int)OrdinalYesterday+1;}
    static int[] GetGregorianTime(double JulianDate){                               //Formula Found Online, Citation Needed.
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
        int[] HourMin = DayFractionToHourMin(dayFraction);
        int[] gregDate = {(int)year,(int)month,(int)days,HourMin[0],HourMin[1],HourMin[2]};
        return gregDate;
        }
    static int[] DayFractionToHourMin(double time){
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
            //Leap seconds 10 seconds at the start of 1972, plus the rest.
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
        double julianCentury = (JulianDate()-millennialJulianDate)/36525;
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
        int[] sunrise = DayFractionToHourMin(sunriseTime);
        int[] sunset = DayFractionToHourMin(sunsetTime);
        int[] riseSetHourMin = {sunrise[0],sunrise[1], sunset[0],sunset[1]};
        return riseSetHourMin;
        }
    }
final class LazyXML{
    private LazyXML(){}
    static Element getElementById(Document myDocument, String IDString){return getElementByIdName(myDocument,IDString,"id");}
    static Element getElementByIdName(Node myDocument, String IDString, String IDName){
        NodeList DocNodeList = myDocument.getChildNodes();
        for(int i=0; i<DocNodeList.getLength();i++){
            if(DocNodeList.item(i).getNodeType() == Node.ELEMENT_NODE){         //End Condition (1 of 2).
                Element el = (Element)(DocNodeList.item(i));
                if(el.getAttribute(IDName).equals(IDString)){return el;}        //End Condition (2 of 2).
                }
            if(DocNodeList.item(i).hasChildNodes()){                            //Recursion Condition.
                Element el =getElementByIdName(DocNodeList.item(i),IDString,IDName);
                if(el != null){return el;}
                }
            }
        return null;}
    static final boolean save(Document myDocument, File myXMLFile){try{
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer        transformer        = transformerFactory.newTransformer();
        DOMSource    source = new DOMSource(myDocument);
        StreamResult result = new StreamResult(myXMLFile);
        transformer.transform(source, result);
        return true;
        }catch(Exception e){return false;}}
    static void cleanWhiteSpace(Node node){
        if(node.hasChildNodes()){
            NodeList nodelist = node.getChildNodes();
            for(int i = nodelist.getLength()-1; i>=0;i--){                      //Bottom to Top, Back to Front. 
                if(    (nodelist.item(i).getNodeType() == Node.TEXT_NODE)           //isTextNode, runs first.
                    && (nodelist.item(i).getNodeValue().trim().isEmpty())){         //isEmpty, runs only if previous is true.
                    node.removeChild(nodelist.item(i));                         //node is parent to nodelist.item(i)
                    }
                else if(nodelist.item(i).hasChildNodes()){cleanWhiteSpace(nodelist.item(i));}
                }
            }
        node.normalize();
        }
    static void NodeListSwap(Node TransactionParent, int child1Index, int child2Index){
        NodeList TransactionList = TransactionParent.getChildNodes();
        //Clones of the Children. Non-Clones won't insert.
        Node child1 = TransactionList.item(child1Index).cloneNode(true);
        Node child2 = TransactionList.item(child2Index).cloneNode(true);
        if(child1Index == TransactionList.getLength()-1){//If is Final Node     //Replace Child 1 with Child 2
            TransactionParent.removeChild(TransactionList.item(child1Index));
            TransactionParent.appendChild(child2);
            }
        else{                                       //Otherwise
            TransactionParent.removeChild(TransactionList.item(child1Index));
            TransactionParent.insertBefore(child2, TransactionList.item(child1Index));
            }
        if(child2Index == TransactionList.getLength()-1){//If is Final Node     //Replace Child 2 with Child 1
            TransactionParent.removeChild(TransactionList.item(child2Index));
            TransactionParent.appendChild(child1);
            }
        else{                                       //Otherwise
            TransactionParent.removeChild(TransactionList.item(child2Index));
            TransactionParent.insertBefore(child1, TransactionList.item(child2Index));
            }
        }
    }
class CreditManager{
    //Define Variables
    File creditXMLFile = new File("credit.xml");
    Document creditsDocument;
    Element creditRecordElement;
    
    CreditManager(){try{                                                        //This try-catch sets up the Document & Element
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder        builder = factory.newDocumentBuilder();
        if(creditXMLFile.isFile()){                                             //If File Exists,
            creditsDocument     = builder.parse(creditXMLFile);                     //Use its Document
            creditRecordElement = creditsDocument.getDocumentElement();             //and its Element
            LazyXML.cleanWhiteSpace(creditRecordElement);                       //Then Clean it.
            //To-Do: Order Transactions
            }
        else{                                                                   //Else, make the File.
            creditsDocument     = builder.newDocument();                            //Use that Document.
            appendEmptyCreditRecordElement(creditsDocument);                        //Create Elements
            creditRecordElement = creditsDocument.getDocumentElement();             //and use them.
            }
        }catch(Exception e){System.out.println("CreditManager did not create Document!\n"+e);}}
    final void save(){
        boolean saved = LazyXML.save(creditsDocument, creditXMLFile);
        if(!saved){System.out.println("CreditManager did not save!");}
        }
    
    private void appendEmptyCreditRecordElement(Document creditsDocument){
        // Root Element: <creditRecord credits="0">
        creditRecordElement = creditsDocument.createElement("creditRecord");            //<creditRecord>
        Attr creditsAttr    = creditsDocument.createAttribute("credits");               //credits
        creditsAttr.setValue("0");                                                      //credits="0"
        creditRecordElement.setAttributeNode(creditsAttr);                              //<creditRecord credits="0">
        creditsDocument.appendChild(creditRecordElement);
        // Level 1 Element: <incomeSource id="incomeSourceNames">
        String[] incomeSourceIDs = {"habit","toDo","event","timer"};            //Note: Each of these has its own code.
        for(String sourceName:incomeSourceIDs){
            Element incomeSourceElement = creditsDocument.createElement("incomeSource");    //<incomeSource>
            Attr    incomeSourceIDsAttr = creditsDocument.createAttribute("id");            //id
            incomeSourceIDsAttr.setValue(sourceName);                                       //id="incomeSourceNames"
            incomeSourceElement.setAttributeNode(incomeSourceIDsAttr);                      //<incomeSource id="incomeSourceNames">
            creditRecordElement.appendChild(incomeSourceElement);                           
            }                                                                               //Note: No Cleaning or normalization necessary.
        }
    
    /* TO DO: Order List for Effeciency. */
    //XML should not be change in non-ordered fashions, so this should only run on initiation.
    private void quickSortTransactions(Node TransactionParent, int lowIndex, int highIndex){
        if(lowIndex < highIndex){
            int p = partitionTransactions(TransactionParent, lowIndex, highIndex);
            quickSortTransactions(TransactionParent,lowIndex,p);
            quickSortTransactions(TransactionParent,p+1,highIndex);
            }
        }
    private int partitionTransactions(Node TransactionParent, int lowIndex, int highIndex){
        double pivot = transactionsTimeValue(TransactionParent,lowIndex);
        int i=lowIndex-1;
        int j=highIndex+1;
        while(true){
            do{i++;}while(transactionsTimeValue(TransactionParent,i)<pivot);
            do{j--;}while(transactionsTimeValue(TransactionParent,j)>pivot);
            if(i>=j){return j;}
            //NodeListSwap(TransactionParent,i,j);
            }
        }
    private double transactionsTimeValue(Node TransactionParent, int i){
        Node transactionNode = TransactionParent.getChildNodes().item(i);
        Element transactionElement = (Element)transactionNode;
        String transactionTime = transactionElement.getAttribute("time");
        return Double.parseDouble(transactionTime);
        }
    /* Incomplete: Oder List for Effeciency. */
    
    void rewardCredits(int credits, String sourceID, String AppID){
        //Create Element: <transaction themePack="themePack" time="JulianTimeConverter.JulianDate()" credits="credits"/>
            Element transactionElement = creditsDocument.createElement("transaction");
            //sourceClassAttr
                Attr AppIDAttr = creditsDocument.createAttribute("AppID");
                AppIDAttr.setValue(AppID);
                transactionElement.setAttributeNode(AppIDAttr);
            //timeAttr
                Attr timeAttr = creditsDocument.createAttribute("time");
                timeAttr.setValue(""+JulianTimeConverter.JulianDate());
                transactionElement.setAttributeNode(timeAttr);
            //creditsAttr
                Attr creditsAttr = creditsDocument.createAttribute("credits");
                creditsAttr.setValue(""+credits);
                transactionElement.setAttributeNode(creditsAttr);
        Element incomeSourceElement = LazyXML.getElementById(creditsDocument,sourceID); //Get Parent  
        if(incomeSourceElement != null){                                        //User-Proof
            incomeSourceElement.appendChild(transactionElement);                //Add Transaction
            //Add Credits to File Total.
                int oldCredits = Integer.parseInt(creditRecordElement.getAttribute("credits"));
                creditRecordElement.setAttribute("credits", ""+(oldCredits + credits));
            }
        }
    
    //To Do: Re make Clear Transaction Functions for ordered Transactions
    //Honestly All these need to be optomized, I'm running shipping beats perfection right now.
    void clearTransactions(double LastJulianDate, String AppID){
        NodeList SourceIDList = creditRecordElement.getChildNodes();
        for(int i=0; i<SourceIDList.getLength();i++){
            NodeList TransactionList = SourceIDList.item(i).getChildNodes();
            for(int j=TransactionList.getLength()-1; j>=0;j--){                 //If times expected to be in order, could be more effecient.
                if(TransactionList.item(j).getNodeType() == Node.ELEMENT_NODE){
                    Element Transaction = (Element)TransactionList.item(j);
                    double TransactionTime = Double.parseDouble(Transaction.getAttribute("time"));
                    String TransactionAppID = Transaction.getAttribute("AppID");
                    if((TransactionTime<LastJulianDate) && (TransactionAppID.equals(AppID))){SourceIDList.item(i).removeChild(Transaction);}
                    }
                else{System.out.println("Non-Element Node in clearTransactions(double LastJulianDate, String AppID)");}
                }
            }
        }
    void clearTransactions(String AppID,double LastJulianDate){             //Orderless.
        clearTransactions(LastJulianDate,AppID);
        }
    void clearTransactions(double LastJulianDate){
        NodeList SourceIDList = creditRecordElement.getChildNodes();
        for(int i=0; i<SourceIDList.getLength();i++){
            NodeList TransactionList = SourceIDList.item(i).getChildNodes();
            for(int j=TransactionList.getLength()-1; j>=0;j--){                 //If times expected to be in order, could be more effecient.
                if(TransactionList.item(j).getNodeType() == Node.ELEMENT_NODE){
                    Element Transaction = (Element)TransactionList.item(j);
                    double TransactionTime = Double.parseDouble(Transaction.getAttribute("time"));
                    if(TransactionTime<LastJulianDate){SourceIDList.item(i).removeChild(Transaction);}
                    }
                else{System.out.println("Non-Element Node in clearTransactions(double LastJulianDate)");}
                }
            }
        }
    void clearTransactions(String AppID){
        NodeList SourceIDList = creditRecordElement.getChildNodes();
        for(int i=0; i<SourceIDList.getLength();i++){
            NodeList TransactionList = SourceIDList.item(i).getChildNodes();
            for(int j=TransactionList.getLength()-1; j>=0;j--){                 
                if(TransactionList.item(j).getNodeType() == Node.ELEMENT_NODE){
                    Element Transaction = (Element)TransactionList.item(j);
                    String TransactionAppID = Transaction.getAttribute("AppID");
                    if(TransactionAppID.equals(AppID)){SourceIDList.item(i).removeChild(Transaction);}
                    }
                else{System.out.println("Non-Element Node in clearTransactions(double AppID)");}
                }
            }
        }
    void clearTransactions(){                                                   //Resets File, Essentially.
        creditsDocument.removeChild(creditRecordElement);                       //Remove Old creditRecordElement
        appendEmptyCreditRecordElement(creditsDocument);                        //Add Empty creditRecordElement
        }
    void clearLastTransaction(String sourceID, String AppID){
        double CurrentTime = JulianTimeConverter.JulianDate();
        Element incomeSourceElement = LazyXML.getElementById(creditsDocument,sourceID); 
        NodeList TransactionList = incomeSourceElement.getChildNodes();
        double latestTransactionTime = 1000.0; //Sufficiently large.
        Node latestTransaction = null;
        for(int j=TransactionList.getLength()-1; j>=0;j--){
            if(TransactionList.item(j).getNodeType() == Node.ELEMENT_NODE){//Should I be assuming the user was being an idiot? Should I clean non-white spaces earlier?
                Element Transaction = (Element)TransactionList.item(j);
                String TransactionAppID = Transaction.getAttribute("AppID");
                if(TransactionAppID.equals(AppID)){
                    double timeSinceTransaction = CurrentTime-Double.parseDouble(Transaction.getAttribute("time"));
                    if(timeSinceTransaction<latestTransactionTime){
                        latestTransactionTime = timeSinceTransaction;
                        latestTransaction = Transaction;
                        }
                    }
                }
            else{System.out.println("Non-Element Node in clearLastTransaction");}
            }
        if(latestTransaction != null){
            incomeSourceElement.removeChild(latestTransaction);
            }
        }
    
    void test(){}
    
    public static void ThemePackManager(){
        //Initialize Registry Directory
        File themePacksDirectory = new File("themePacks");
        if(!themePacksDirectory.isDirectory()){themePacksDirectory.mkdir();} 
        //System.out.println("Line 004 [Success]: Directory \"themePacks\"                            Initinalized.");
        
        //Initialize Theme
        File     theme         = new File("themePacks\\~theme.xml");
        Document themeDocument = null;
        Element  themeElement  = null;
        boolean  isUpToDate    = true;
        //System.out.println("Line 011 [Success]: ~theme.xml                                        Variables Initialized.");
        try{                                                                    //This try-catch sets up the Theme's Document & Element 
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder        builder = factory.newDocumentBuilder();
            if(theme.isFile()){                                                     //If isFile,
                //System.out.println("Line 016 [Success]: ~theme.xml                                        Is File.");
                themeDocument = builder.parse(theme);                                   //Acknowledge Document
                themeElement  = themeDocument.getDocumentElement();                     //Acknowledge Element
                File[] themePacks = themePacksDirectory.listFiles();                    //Check isUpToDate
                for(File pack:themePacks){isUpToDate = pack.lastModified()<theme.lastModified() && isUpToDate;}
                }
            else{                                                                  //If !isFile, make File.
                //System.out.println("Line 024 [Success]: ~theme.xml                                        Is NOT File.");
                themeDocument = builder.newDocument();                                  //Create Document.
                themeElement  = themeDocument.createElement("theme");                   //Create Element.
                themeDocument.appendChild(themeElement);                                //(Add Element only to remove later in code.)
                isUpToDate    = false;                                                  //Assume !isUpToDate
                }
            //System.out.println("Line 029 [Success]: ~theme.xml                                        IsUpToDate: "+isUpToDate);
            }catch(Exception e){System.out.println("Line 031 [Failure]: ThemePackManager did not create theme File or Document!\n"+e);}
        
        //To Do: Manage isUpToDate
        if(isUpToDate){                                                         //If isUpToDate
            LazyXML.cleanWhiteSpace(themeElement);                                  //Clean it. 
            //System.out.println("Line 036 [Success]: ~theme.xml                                        Cleaned.");
            }
        else{                                                                  //If !isUpToDate, Reset File. 
            themeDocument.removeChild(themeElement);                                //Remove Old Element
            //Root Element: <theme>                                                 //Create Base Elements
            themeElement = themeDocument.createElement("theme");            
            themeDocument.appendChild(themeElement);
            // Level 1 Element: <incomeSource id="incomeSourceNames">
            String[] incomeSourceIDs = {"habit","toDo","event","timer"};        //Note: Each of these has its own code.
            for(String sourceName:incomeSourceIDs){
                Element incomeSourceElement = themeDocument.createElement("incomeSource");      //<incomeSource>
                Attr    incomeSourceIDsAttr = themeDocument.createAttribute("id");              //id
                incomeSourceIDsAttr.setValue(sourceName);                                       //id="incomeSourceNames"
                incomeSourceElement.setAttributeNode(incomeSourceIDsAttr);                      //<incomeSource id="incomeSourceNames">
                themeElement.appendChild(incomeSourceElement);                           
                }
            //System.out.println("Line 052 [Success]: ~theme.xml                                        File Reset.");
            //Note: No Cleaning or normalization necessary.
            
            
            //Initialize Registry
            File     themePackReg         = new File("themePacks\\themePackReg.xml");
            Document themePackRegDocument = null;
            Element  themePackRegElement  = null;
            //System.out.println("Line 060 [Success]: themePackReg.xml                                  Variables Initialized.");
            try{                                                                    //This try-catch sets up the Registry's Document & Element 
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder        builder = factory.newDocumentBuilder();
                if(themePackReg.isFile()){                                              //If File Exists, use it.
                    //System.out.println("Line 065 [Success]: themePackReg.xml                                  Is File.");
                    themePackRegDocument = builder.parse(themePackReg);                     //Acknowledge Document
                    themePackRegElement  = themePackRegDocument.getDocumentElement();       //Acknowledge Element
                    LazyXML.cleanWhiteSpace(themePackRegElement);                           //Clean it.
                    }
                else{                                                                  //Else, make the File.
                    //System.out.println("Line 071 [Success]: themePackReg.xml                                  Is NOT File.");
                    themePackRegDocument = builder.newDocument();                           //Create Document.
                    //!appendEmptyElement(themePackRegDocument);                              //To Do: Create Drfault Elements
                    themePackRegElement  = themePackRegDocument.getDocumentElement();       //and use them.
                    }
                }catch(Exception e){System.out.println("Line 076 [Failure]: ThemePackManager did not create Registry Document!\n"+e);}
            
            
            //Add Elements from Each themePack
            Document themePackDocument  = null;
            Element  themePackElement   = null;
            NodeList themePackList      = themePackRegElement.getChildNodes();
            //System.out.println("Line 083 [Success]: themePack:null                                    Variables Initialized.");
            for(int i=0;i<themePackList.getLength();i++){                                   //Check Each File
                String fileName = ((Element)themePackList.item(i)).getAttribute("file");
                boolean load = Boolean.parseBoolean(((Element)themePackList.item(i)).getAttribute("load"));
                if(load){try{                                                               //If set to load, load themePack
                    //System.out.println("Line 088 [Success]: themePack:"+i+"                                       Set to load.");
                    File themePack = new File("themePacks\\"+fileName);
                    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();  
                    DocumentBuilder        builder = factory.newDocumentBuilder();
                    if(themePack.isFile()){                                                 //If File Exists, use it.
                        //System.out.println("Line 093 [Success]: themePack:"+i+"                                       Is File.");
                        themePackDocument = builder.parse(themePack);                           //Acknowledge Document
                        themePackElement  = themePackDocument.getDocumentElement();             //Acknowledge Element
                        LazyXML.cleanWhiteSpace(themePackElement);                              //Clean it.
                                                                                                //Then...
                        NodeList IncomeSourceNodes = themePackElement.getChildNodes();          
                        for(int j=0;j<IncomeSourceNodes.getLength();j++){                                           //For-Each      Income-Source in themePack
                            Element  themePackIncomeSource = (Element)IncomeSourceNodes.item(j);                         //Get IncomeSource
                            NodeList themePackNodes        = themePackIncomeSource.getChildNodes();                      //Get IncomeSource's Nodes
                            String   IncomeSourceType      = themePackIncomeSource.getAttribute("id");                   //Get IncomeSource's ID
                            Element  themeIncomeSource     = LazyXML.getElementById(themeDocument, IncomeSourceType);    //Get IncomeSource in theme
                            NodeList themeNodes            = themeIncomeSource.getChildNodes();                          //Get IncomeSource in theme's Nodes
                            //System.out.println("Line 105 [Success]: themePack:"+i+" IncomeSource:"+j+"                        Variables Initialized.");
                            
                            for(int k=0;k<themePackNodes.getLength();k++){                          //For-Each Node in themePack Income-Source.
                                boolean  replacedNode  = false;                                     //Assume theme doesn't Contain Node
                                Element  themePackNode      = (Element)themePackNodes.item(k);          //Get Node
                                String   themePackNodeAppID = themePackNode.getAttribute("AppID");      //Get Node's AppID
                                //System.out.println("Line 111 [Success]: themePack:"+i+" IncomeSource:"+j+" PackNode:"+k+"             Variables Initialized.");
                                
                                //Compare themePack's Node to theme Nodes.
                                if(themeNodes.getLength() > 0){
                                        for(int l=0;l<themeNodes.getLength();l++){                              
                                            Element themeNode  = (Element)themeNodes.item(l);        //Get theme Node
                                            String  themeAppID = themeNode.getAttribute("AppID");    //Get theme Node's AppID
                                            replacedNode = themeAppID.equals(themePackNodeAppID);    //This is used outside of the loop.
                                            //System.out.println("Line 118 [Success]: themePack:"+i+" IncomeSource:"+j+" PackNode:"+k+" ThemeNode:"+l+" Variables Initialized.");
                                            if(replacedNode){                                                       //If Same, Replace
                                                themeIncomeSource.removeChild(themeNodes.item(l));                                                                                        //Remove
                                                if(l == themeNodes.getLength()-1){  themeIncomeSource.appendChild(themeDocument.importNode(themePackNode, true));}                        //Append
                                                else{                               themeIncomeSource.insertBefore(themeDocument.importNode(themePackNode, true), themeNodes.item(l));}   //or Insert
                                                break;
                                                }
                                            }
                                        if(!replacedNode){                          themeIncomeSource.appendChild(themeDocument.importNode(themePackNode, true));}    //If No Replacement, Append
                                    }
                                else{                                               themeIncomeSource.appendChild(themeDocument.importNode(themePackNode, true));}                         //If Empty, Append
                                //Compare themePack's Node to theme Nodes.
                                
                                }
                            }
                        }
                    else{                                                                      //If Files doesn't exists, continue.
                        System.out.println("Line 136 [Failure]: themePack"+i+" is NOT File.");      //...
                        continue;                                                                   //continue.
                        }                                                       
                    }catch(Exception e){System.out.println("Line 139 [Failure]: ThemePackManager did not load "+fileName+"!\n"+e);continue;}}
                }
            }
        LazyXML.save(themeDocument,theme);
        }
    }


public class XMLApp {
    public static void main(String[] args){
        /*
        CreditManager cm = new CreditManager();
        cm.clearLastTransaction("habit", "mypack");
        cm.test();
        cm.save();
        */
        
    
        String testStr = "\\a\\\"\b\0";
        System.out.println(testStr);
        testStr = cleanSQLightTxt(testStr);
        System.out.println(testStr);
        }
    static String cleanSQLightTxt(String str){
        str = str.replace("\b","\\b");
        str = str.replace("\n","\\n");
        str = str.replace("\r","");
        str = str.replace("\t","\\t");
        //str = str.replace("\Z","\\Z");
        //str = str.replace("\%","\\%");
        //str = str.replace("\_","\\_");
        str = str.replace("\\","\\\\");
        str = str.replace("\"","\\\"");
        return str;
        }
    }
