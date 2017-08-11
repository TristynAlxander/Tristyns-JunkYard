package txtcombiner;
import java.io.*;
import java.util.*;
public class TXTCombiner {
    public static void main(String[] args) throws IOException{
        //Figure out what you have
        
        //Get & Figure valid input files
        File ins = new File("inputs");
        if(!ins.exists()){System.out.println("Doesn't Exist!");}
        if(!ins.isDirectory()){System.out.println("Not Directory!");}
        List<File> Inins = new ArrayList<>(Arrays.asList(ins.listFiles()));
        for(int i=0; i<Inins.size();i++){
            File filei = Inins.get(i);
            if(filei.isDirectory()){Inins.remove(i);i--;}
            else if(!filei.getName().endsWith(".txt")){Inins.remove(i);i--;}
            else if(filei.getName().contains("+")){Inins.remove(i);i--;}
            }
        
        //Get Base input names
        ArrayList<String> BaseTxtList = new ArrayList<>();
        for(int i=0; i<Inins.size();i++){
            File filei = Inins.get(i);
            String S =filei.getName().substring(0, filei.getName().length() - 4);
            BaseTxtList.add(S);
            }
        
        //Make To MakeList
        ArrayList<String> ToMakeTxtList = new ArrayList<>();
        TODOListRecursive(BaseTxtList,ToMakeTxtList,"",0);
        
        // if the directory does not exist, create it
        File outputs = new File("outputs");
        if (!(outputs.exists() && outputs.isDirectory())) {
            if(!outputs.isDirectory()){outputs.delete();}
            try{outputs.mkdir();} 
            catch(SecurityException e){System.out.println("Security Exception");}        
            }
        else{System.out.println("Already Exists");}
        
        //Make Output Files
        MakeOutFiles(ToMakeTxtList);
        }
    public static void TODOListRecursive(ArrayList<String> BaseTxtList, ArrayList<String> ToMakeTxtList, String str,int k){
        for(int i=k;i<BaseTxtList.size();i++){
            String S= str+"+"+BaseTxtList.get(i);
            String FileName = S.substring(1)+".txt";
            ToMakeTxtList.add(FileName);
            TODOListRecursive(BaseTxtList,ToMakeTxtList,S,i+1);
            }
        }
    public static void MakeOutFiles(ArrayList<String> ToMakeTxtList) throws IOException{
        for(String fileName: ToMakeTxtList){
            String FileLocation = "outputs/"+fileName;
            PrintWriter writer = new PrintWriter(FileLocation, "UTF-8");
            String[] subFileNames = fileName.split("\\+");
            for(String subFileName:subFileNames){
                //Name to Location
                if(!subFileName.endsWith(".txt")){subFileName=subFileName+".txt";}
                String Location="inputs/"+subFileName;
                
                //Write it
                String subFileAsStr =FileToStr(Location);
                writer.println(subFileAsStr);
                }
            writer.close();
            }
        }
    public static String FileToStr(String fileLocation) throws IOException{
        String outStr = "";
        Scanner readf = new Scanner(new File(fileLocation));
        while(readf.hasNextLine()){outStr =outStr + readf.nextLine()+"\n";}
        return outStr;
        }
}
