/*
# (C) 2010 Jost Berthold (berthold at diku.dk), grid.dk
#          E-science Center, Copenhagen University
# This file is part of ESS-McStas solutions.
# 
# ESS-McStas solutions is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ESS-McStas solutions is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */
/* submit one job given as a dictionary. EXECUTE must be defined,
 * no field names unknown to MiG mRSL should be given.
 *
 * Arguments: job dictionary, callbacks for success and error case
 * Returns: nothing.
 */ 
function mig_submit_dict(dict, callback_ok, callback_error) {

    /* take the result of a job submission, extract the job-ID if
     * successful, all error messages otherwise. Only one job
     * submission is expected, not multiple results.
     *
     * Arguments: json result of job submission (submitfields.py)
     * Returns (boolean,string), with String being either a job_id
     * or a concatenation of error messages enclosed in <p>..</p>
     */
    function extract_result(jsonRes) {
           
        var errors="";
        var job_id="";
        for(var i=0; i<jsonRes.length; i++) {
      
            switch(jsonRes[i]["object_type"]) {
                
            case "error_text":
                errors +="<p>"+jsonRes[i].text+"</p>";
                break;
          
            case "submitstatuslist":
                   
                // we only expect one job, not several
                if (jsonRes[i]["submitstatuslist"].length > 1) {
                    errors += "<p>Unexpected: multiple submission results</p>";
                    break;
                }
                   
                if (jsonRes[i]["submitstatuslist"][0]["status"]) {
                    job_id = jsonRes[i]["submitstatuslist"][0]["job_id"];
                } else {
                    errors += "<p>" 
                               + jsonRes[i]["submitstatuslist"][0]["message"] 
                               + "</p>";
                }
                break;
                   
            case "text":
                errors += "<p>" + jsonRes[i]["text"] + "</p>";
                break;
          
            default:
                // skip
            }
            // stop as soon as job_id is found
            if (job_id != "") {
                return [true,job_id];
            }
        }

        // we reach here, so no job_id has been found
        if (errors == "") {
            errors = "<p>Invalid reply (no job id, no errors)</p>";
        }
        return [false, errors];
    }
       

    // make sure we have an "EXECUTE" field
    if (dict.EXECUTE == undefined || dict.EXECUTE == "") {
        callback_error("<p>No EXECUTE sequence given.</p>");
        return;
    }

    // do the job submission
    $.getJSON("submitfields.py", dict, 
              function(reply, statusText) {
                  var res = extract_result(reply);
                  var success = res[0];
                  var message = res[1];
                  if (success) {
                      callback_ok(message);
                  } else {
                      callback_error(message);
                  }
    });

}


/* submission of a simulation job:
 * 
 * Assumes a form with ID "name" (as generated by jobpage.pl) to 
 * set simulation parameters and using ID <name> in the html which
 * imports this script. Inside the form (id="name"), the following:
 *  - Input fields with class .sim_parameter 
 *     All parameter fields. Field Name==parameter name, all mandatory.
 *  - option fields, first one inside form taken. Class names are
 *    .sim_neutrons, .sim_gravitation, .sim_extra, .sim_files
 * Furthermore, an area with id "messages" in the page, for messages.
 *  
 * A corresponding file <name>.c is assumed to exist in the same
 * directory as the html file (not checked!).
 *
 * A global variable mcstas_vgrid is assumed (for output destination).
 */

function simjob_submit(name) {
    
    if (mcstas_vgrid == undefined) {
        alert("Setup error: VGrid unknown.");
        return;
    }

    // to abort if we are not ready to submit
    $( "#messages" ).html(""); // empty messages
    var abort = false;

    var paramlist = [];
    var p_len = 0;

    // build "other" sim options (first on cmd. line)
    var neutrons = $( "#" + name + " .sim_neutrons" )[0].value;
    if (!(neutrons == '')) {
        paramlist[p_len++] = "-n " + neutrons; 
    }
    var gravi = $( "#" + name + " .sim_gravitation" )[0].checked;
    if (gravi) {
        paramlist[p_len++] = "-g";
    }

    // set the output file name, use a MIG variable
    var out_file = name + "_+JOBID+.sim";
    paramlist[p_len++] = "-f " + out_file;

    // put in all parameters from the user in one element
    paramlist[p_len++] = $( "#" + name + " .sim_extra" )[0].value;

    // select parameters and build list
    // complain if we do not have a parameter value
    $( "#" + name + " .sim_parameter" ).each(function(i) {
        if (this.value == "") {
            $( "#messages").append("Missing parameter value "
                                   + this.name + "<br/>");
            abort = true;
            return;
        }
        paramlist[p_len++] = this.name + "=" + this.value;
        return;
    });

    if (abort) { return; };

    var run_params = paramlist.join(" ");

    /* find out where we are: concat vgrid_name= and file= part.
     * We cannot simply use the file= part and mcstas_vgrid, since
     * the mcstas_vgrid value might differ from vgrid_name in
     * the URL.
     */  
    // default:
    var path_prepend = "private_base/" + mcstas_vgrid + "/compiled";
    var match = 
        (location.search).match("vgrid_name=([^&]+)&path=([^&]*/)[^/]+\.html") 
        || ["",mcstas_vgrid,"compiled/"];
    path_prepend = "private_base/" + match[1] + "/" + match[2];

    // treat input files given by the user

    var extra_files = 
        ($( "#" + name + " .sim_files" )[0].value || "").split("\n");
    $.each(extra_files, function(i,str) {
        var base = str.match(/\/([^/]+$)/);
        if (base != undefined) {
            extra_files[i] = str + "\t " + base[1];
        }
    });
    var in_files = path_prepend + name + ".c\t " + name + ".c\n" 
                   + extra_files.join("\n");

    abort = !(confirm("Compile "+name+".c, run program with:\n\"" 
                      + run_params + "\".\n" 
                      + "Extra files: " + extra_files.join(" ")
                      + "\n\nSubmit this job?"));

    if (abort) { return; };

    // Job can run anywhere, assuming a C compiler "cc".
    // TODO: check McStas compilation options, state RE "CC"
    //  _FORTIFY_SOURCE has to be disabled for ubuntu machines :)
    var exec = "cc -g -O2 -lm -U_FORTIFY_SOURCE " + name + ".c \n" 
             + "./a.out " + run_params;

    var dict = {"output_format":"json",
                "RUNTIMEENVIRONMENT": "",
                "VGRID": "ANY",
                "JOBNAME": "run-" + name,
                "OUTPUTFILES": out_file + "\t private_base/" + mcstas_vgrid 
                               + "/simulated/" + out_file + "\n",
                "INPUTFILES" : in_files,
                "EXECUTE": exec
                };

    /* We could check existence of C code (same directory)
     * This has to be done using ajax/getJSON (ls.py) 
     */

    mig_submit_dict(dict, 
        // callback for success:
        function(job_id) {
            $( "#messages" ).append("Submitted job: " 
                                    + job_id + "<br/>");
            out_file = name + "_" + job_id + ".sim";
            $("#messages" ).append("output file: <a href='/vgrid/"
                                   + mcstas_vgrid + "/path/simulated/" 
                                   + out_file + "'>simulated/" 
                                   + out_file + "</a><br/>");
            alert("Your simulation job has been submitted.\n" 
                  + "Results will appear as " + out_file);
        },
        // callback for errors
        function(errors) {
            $( "#messages" ).append("<div class='errortext'>Errors: " 
                                    + errors + "</div>");
            alert("Job submission not successful!");
    });
    return;

}


/* submission of a compilation job
 * 
 * Uses fixed naming scheme for fields in the web form: 
 *   #file_name    - path to instr., checked to match "*.instr"
 *   #output_dir   - receives html and c, default: mcstas_vgrid + "/compiled"
 *   #custom_comps - component files to provide for compilation
 * 
 * Global variables assumed: 
 *   mcstas_vgrid, for file input and output
 *   mcstas_re, name of runtime env providing MCSTAS,MCSTAS_C; MCDISPLAY
 */
function compile_submit() { 

    if (mcstas_vgrid == undefined || mcstas_re == undefined) {
        alert("Setup error: VGrid or Runtime Env. unknown.");
        return;
    }

    var file_name = $( "#file_name" )[0].value;

    // check and truncate file name
    if (file_name == "") {
        alert("Error: No file to compile given.");
        return;
    }
    var match = file_name.match(new RegExp("^(.*/)?([^/]+)\.instr"));
    var base_name;
    if (match == null) {
        alert(file_name + ": invalid name (should end in \"instr\")");
        return;
    } else {
        base_name = match[2];
    }

    // use explicit output destination if given
    var output_dir = "private_base/" + mcstas_vgrid + "/compiled/";

    match = $( "#output_dir" )[0].value;
    if (match != "") {
        output_dir = match;
        if (output_dir[output_dir.length-1] != "/") {
            output_dir += "/";
        }
    }

    // write back the instrument to the output dir
    var suffix = [".instr", ".c", ".html"];
    var out_files = ""; // will build multiline string OUTPUTFILES
    var i;
    for (i=0; i < suffix.length; i++) {
        var n = base_name + suffix[i];
        out_files += n + "\t" + output_dir + n + "\n";
    }

    var in_files = file_name + " " + base_name + ".instr\n" 
                   + "private_base/" + mcstas_vgrid + "/head.temp head.temp\n"
                   + "private_base/" + mcstas_vgrid + "/tail.temp tail.temp\n"
                   + $( "#custom_comps" )[0].value;

    var exec = "$MCSTAS_C " + base_name + ".instr\n"
                + "./jobpage.pl -d --content-only -o temp.html -v " + mcstas_vgrid + " " + base_name + ".instr \n"
                // + "PARAMS=`$JOBPAGE_GEN -p --content-only -o temp.html -v " + mcstas_vgrid + " " + base_name + ".instr` \\\n"
                // + "cc -g -O2 -DMC_TRACE_ENABLED -lm " + base_name + ".c -o " + base_name + ".out && \\\n"
                // + "$MCDISPLAY -gif -m " + base_name + ".out $PARAMS \n";
                // mcdisplay unused for now
                + "cat head.temp temp.html tail.temp > " + base_name + ".html\n";

    var dict = {"output_format":"json",
                "RUNTIMEENVIRONMENT": mcstas_re,
                "VGRID": mcstas_vgrid,
                "JOBNAME":"compile-" + base_name,
                "OUTPUTFILES": out_files,
                "INPUTFILES" : in_files,
                "EXECUTE":exec,
                "EXECUTABLES": "private_base/" + mcstas_vgrid 
                               + "/jobpage.pl jobpage.pl"
    };

    mig_submit_dict(dict, 
            // callback for success:
        function(job_id) {
            $( "#result" ).append("Submitted job: " + job_id + "<br/>");
            $( "#result" ).append("output directory: <a href='"
                                  + output_dir.replace(
                                          "private_base/" + mcstas_vgrid,
                                          "/vgrid/" + mcstas_vgrid + "/path")
                                  + "'>" + output_dir + "</a><br/>");
        },
        // callback for errors
        function(errors) {
            $( "#result" ).append("<div class='errortext'>Errors: " 
                                  + errors + "</div>");
    });

    return;
}


/* submission of a visualisation job
 * 
 * Uses fixed naming scheme for fields in the web form: 
 *   #file_name    - path to instr., checked to match "*.sim"
 *   #out_opt      - drop-down for choosing ps, color ps, or gif format
 *   #output_dir   - receives html and c, default: mcstas_vgrid + "/simulated"
 * 
 * Global variables assumed: 
 *   mcstas_vgrid, for file input and output
 *   mcstas_re, name of runtime env providing MCSTAS,MCSTAS_C; MCDISPLAY
 */
function viz_submit() { 

    if (mcstas_vgrid == undefined || mcstas_re == undefined) {
        alert("Setup error: VGrid or Runtime Env. unknown.");
        return;
    }

    var file_name = $( "#file_name" )[0].value;

    // check and truncate file name
    if (file_name == "") {
        alert("Error: No file given.");
        return;
    }
    var match = file_name.match(new RegExp("^(.*/)?([^/]+)\.sim"));
    var base_name;
    if (match == null) {
        alert(file_name + ": invalid name (should end in \"sim\")");
        return;
    } else {
        base_name = match[2];
        // prepend vgrid path and "simulated" directory if none given
        if (match[1] == undefined) {
            file_name = "private_base/" + mcstas_vgrid 
                        + "/simulated/" + file_name;
        }
    }

    // get output option:
    var out_opt = $( "#out_opt" ).val();
    var suffix;
    switch (out_opt) {
        case "-gif": suffix = "gif";
                     break;
        case "-ps" :
        case "-psc": suffix = "ps";
                     break;
    }

    // use explicit output destination if given
    var output_dir =  "private_base/" + mcstas_vgrid + "/simulated/";

    match = $( "#output_dir" )[0].value;
    if (match != "") {
        output_dir = match;
        if (output_dir[output_dir.length-1] != "/") {
            output_dir += "/";
        }
    }

    // write back picture to output dir as "base_name.sim.suffix"
    var out_files = base_name + ".sim." + suffix + "\t " 
                    + output_dir + base_name + ".sim." + suffix;

    var dict = {"output_format":"json",
                "RUNTIMEENVIRONMENT": mcstas_re,
                "VGRID": mcstas_vgrid,
                "JOBNAME":"viz-" + base_name,
                "OUTPUTFILES": out_files,
                "INPUTFILES" : file_name + "\t " + base_name + ".sim",
                "EXECUTE": "$MCPLOT " + base_name + ".sim " + out_opt
               };

    mig_submit_dict(dict, 
        // callback for success:
        function(job_id) {
            $( "#result" ).append("Submitted job: " + job_id + "<br/>");
            $( "#result" ).append("output directory: <a href='fileman.py?path="
                    // use output_dir here, should always work
                                  + output_dir + "'>" 
                                  + output_dir + "</a><br/>");
        },
        // callback for errors
        function(errors) {
            $( "#result" ).append("<div class='errortext'>Errors: " 
                                  + errors + "</div>");
    });

    return;
}
