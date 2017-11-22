
# ----- TYPE DEFINITIONS

type file;

# ----- APP DEFINITION

app (file out) preProcess (file execute, file input)
{
   python2 @execute @input stdout=@out;
}

app (file out, file csv, file sout,file serr) runEP (file execute, file input, string casename, file bashscript)
{
   bashRun "run.sh"  @execute @input casename @out @csv stdout=@sout stderr=@serr;
}

app (file out, file csv, file sout,file serr) postProcess (file execute, file[] cases,file[] casescsv, file[] casesout, file[] caseserr, file bashscript)
{
     bashRun "postprocess.sh"  @execute @out @csv stdout=@sout stderr=@serr;
}

# ----- INPUTS & OUTPUTS

  # inputs
  file input 	    <arg("epzip")>;

  # outputs
  file finalresults <arg("results")>;
  file totalcsv <arg("total")>;
  
  # supporting files
  file PREPROCESS 	<"preprocess.py">;
  file RUNEP		<"run.py">;
  file POSTPROCESS	<"postprocess.py">;
  
  file runBash		<"run.sh">;
  file runPostprocess	<"postprocess.sh">;
  
#  string outpath="results";
  
# ----- PARAMETER SETUP & LAUNCH

  # first get available cases
  file outf <"cases.list">;
  outf = preProcess(PREPROCESS,input);
  string[] caseNames = readData(outf);
  trace("\n" + length(cases) +" Cases in simulation\n");
  trace(caseNames[0]);

  file[] cases;
  file[] casescsv;
  file[] casesout;
  file[] caseserr;
  foreach caseName, i in caseNames {
        file runcase    <strcat("results/",caseName,".tgz")>;
        file casecsv  	<strcat("results/",caseName, "_total",".csv")>;
    	file caseout    <strcat("results/logs/out/",caseName,".out")>;
    	file caseerr    <strcat("results/logs/err/",caseName,".err")>;
  
    	(runcase, casecsv, caseout,caseerr) = runEP(RUNEP,input,caseName,runBash);
    	cases[i] = runcase;
    	casescsv[i] = casecsv;
    	casesout[i] = caseout;
    	caseserr[i] = caseerr;
  }

trace(filenames(cases));
  file pout    <strcat("results/logs/out/post.out")>;
  file perr    <strcat("results/logs/err/post.err")>;
  (finalresults, totalcsv, pout,perr) = postProcess(POSTPROCESS,cases,casescsv,casesout,caseserr,runPostprocess);

  
