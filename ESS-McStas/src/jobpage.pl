#! /usr/bin/perl -w

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

# This script is an adaption of mcdoc to a specific purpose: It
#  generates a html page with a description of the instrument,
#  including a web form to submit a simulation job.
#
# Author: Jost Berthold, berthold at diku.dk
#         E-science Center, Copenhagen University
#
# Also see: http://www.mcstas.org.

# Determine the path to the McStas system directory. This must be done
# in the BEGIN block so that it can be used in a "use lib" statement
# afterwards.

use Config;
use Cwd;
BEGIN {
  # default configuration (for all high level perl scripts)
  if($ENV{"MCSTAS"}) {
    $MCSTAS::sys_dir = $ENV{"MCSTAS"};
  } else {
    if ($Config{'osname'} eq 'MSWin32') {
      $MCSTAS::sys_dir = "c:\\mcstas\\lib";
    } else {
      $MCSTAS::sys_dir = "/usr/local/lib/mcstas";
    }
  }
  $MCSTAS::perl_dir = "$MCSTAS::sys_dir/tools/perl";
}

use lib $MCSTAS::perl_dir;
require "mcstas_config.perl";

# Overload with user's personal config
if ($ENV{"HOME"} && -e $ENV{"HOME"}."/.mcstas/mcstas_config.perl") {
  require $ENV{"HOME"}."/.mcstas/mcstas_config.perl";
}

use FileHandle;
use File::Basename;
require "mcrunlib.pl";

# write an error message including usage information
# then abort the program ( complain never returns )
sub complain {
    my ($msg) = @_;
    system("$0 -h");
    die "\n$0: $msg\n";
}

# global verbosity and param (HAAAAACK) options
my $verbose=0;
my $params="";

# URL for private vgrid pages is /vgrid/$mcstas_vgrid
# For file upload/download (relative to the user home), it is
# vgrid_private_base/$mcstas_vgrid

# THESE CAN BE MODIFIED BY SCRIPT PARAMETERS
#my $mig_dns = "localhost:10443";
my $mcstas_vgrid = "mcstas-vgrid";

# jquery path, goes into the header
# should contain jquery-1.3.2.min.js and jquery-ui-1.7.2.custom.min.js
# (MiG installation provides them. We will later use the following:

# my $jquery_path = http://$mig_dns/images/js;

my $jquery_path = ".";
my @jquery_libs = (  "jquery-1.3.2.min.js" 
		   , "jquery.migtools.js" 
		   # , "jquery-ui-1.7.2.custom.min.js"
		   );

# this can (and will) go into the body, close to the form which calls it
my $simjob_submit_js = <<'END_JS';
<!-- catch errors due to missing jquery.migtools.js -->
<script type="text/javascript" >

    if (simjob_submit == undefined) {
        var simjob_submit = function(name) { 
              alert("Setup error: Required javascript missing."); 
	};
    }
</script>
END_JS

# Output a HTML form for input parameters.
# - Field names are parameter names, defaults are pre-filled.
# - Form submission triggers a javascript method (to be defined)
#   which takes the instrument name as a string parameter.
#   The form carries the instrument name as ID as well.
# parameters: file handle, parameters, parameter details (?), name to use

sub gen_submission_form {
    
    my ($f, $ps, $qs, $name) = @_;
    my $i;

    print $f $simjob_submit_js;
    print $f "<!-- sim.job submission form, generated -->\n";
    print $f "<form id='$name' ",
             "action=\"javascript:simjob_submit('$name');\" method='post' >\n";

    # Generate a table to set the parameters.
    print $f " <TABLE id='$name",
             "_param' style='margin-right:200px;width:80%;'>\n";
    print $f "   <TR><TH COLSPAN='4' >Instrument Parameters</TH></TR>\n",
             "   <TR><TH>Name</TH> <TH>Default</TH>",
    "       <TH>Unit</TH> <TH>Description</TH></TR>\n";
    # Avoid outputting empty table.
    if (@$ps == 0) {
        print $f "<tr><td colspan='4'>",
	         "No instrument parameters to set.</td></tr>\n";
    } else {
	for $i (@$ps) {
	    my $default = $qs->{$i}{'default'};
	    $params .= " $i=";
	    if ( defined($default) ) {
		$params .= $default;
	    } else { 
		$params .= "0"; 
		$default = ""; # for subsequent output
	    }
	    print $f "   <TR> <TD>";
	    print $f "<B>" unless defined($default);
	    print $f "$i";
	    print $f "</B>" unless defined($default);
	    print $f "</TD>\n";
	    print $f "   <TD >", 
	        "<input class='sim_parameter' type='text' size='20'",
	        " name='$i' value='$default' /></TD>\n";
	    if($qs->{$i}{'unit'} && $qs->{$i}{'text'}) {
		print $f "     <TD>$qs->{$i}{'unit'}</TD>";
		print $f "     <TD>$qs->{$i}{'text'}</TD>";
	    } else {
		print $f "     <TD>-</TD> <TD>(no description found)</TD>";
	    }
	    print $f "</TR>\n";
	}
    }

    # TODO: set simulation options: no. of neutrons, output file name,
    # and maybe allow free-form extra options (?)
    print $f "<tr><th colspan=\"4\">Other simulation options</th></tr>\n";
    print $f "<tr><td>Neutrons</td><td><input class='sim_neutrons'",
             " type='text' name='sim_neutrons' /></td><td/>",
             "<td>Number of neutrons to simulate</td></tr>\n";
    print $f "<tr><td>Gravitation</td><td><input class='sim_gravitation'",
             " type='checkbox' name='sim_gravitation' /></td><td/>",
             "<td>include gravitation forces in computation?</td></tr>\n";

    print $f "<tr><td>Extra parameters</td><td><input class='sim_extra'",
             " type='text' name='sim_extra' /></td><td/>",
             "<td>other parameters added to the command line</td></tr>\n";

    print $f "<tr><th colspan='4'>Data files</th></tr>\n",
             "<tr><td colspan='3'>\n",
             "<textarea cols='60' rows='4' class='sim_files'>",
             "</textarea></td>\n",
             "<td>Specify data files to send with the simulation job<br/>",
             "(one per line)</td>\n</tr>\n";

    print $f "<tr><td/><td>",
             "<input type='submit' value='Submit simulation job' />\n";
    print $f "<td colspan='2' id='messages' style='color:red'>",
             "<!--filled by js--></td></tr>";
    print $f "</TABLE>\n";
    print $f "</form> <!-- $name","_submit -->\n";
}

#
# Output the HTML table for either input or output parameters.
# Here, used for output parameters only.
#
sub gen_param_table {
    
    my ($f, $ps, $qs) = @_;
    my $i;
    # Avoid outputting empty table.
    unless(@$ps) {
        print $f "None.\n";
        return;
    }
    print $f "<TABLE BORDER=1>\n";
    print $f "<TR><TH>Name</TH>  <TH>Unit</TH>  <TH>Description</TH> <TH>Default</TH></TR>\n";
    for $i (@$ps) {
        my $default = $qs->{$i}{'default'};
        print $f "<TR> <TD>";
        print $f "<B>" unless defined($default);
        print $f "$i";
        print $f "</B>" unless defined($default);
        print $f "</TD>\n";
        if($qs->{$i}{'unit'} && $qs->{$i}{'text'}) {
            print $f "     <TD>$qs->{$i}{'unit'}</TD>\n";
            print $f "     <TD>$qs->{$i}{'text'}</TD>\n";
        } else {
            print $f "     <TD></TD> <TD></TD>\n";
        }
        print $f "<TD ALIGN=RIGHT>", defined($default) ?
            $default : "&nbsp;", "</TD> </TR>\n";
    }
    print $f "</TABLE>\n\n";
}

#
# Generate description web page from component with information in $d.
# parameters: ($data, $basename, $name);
sub gen_html_description {
    my ($d, $bn, $n) = @_;
    my $f = new FileHandle;
    my $is_opened = 0;

    if (!(open($f, ">$bn.html"))) { # use component location for name
      complain("could not open file $bn.html. Aborting execution.");
    }

    if ( !$content_only ) {
	print $f "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2//EN\">\n";
	print $f "<HTML><HEAD>\n";
	print $f "<TITLE>McStas: $d->{'name'} $d->{'type'} at $d->{'site'}</TITLE>\n";
	print $f "<LINK REV=\"made\" HREF=\"mailto:peter.willendrup\@risoe.dk\">\n";
	print $f "<LINK REV=\"made\" HREF=\"berthold at diku.dk\">\n";
	print $f "<link rel='stylesheet' type='text/css' " . 
	         "href='./mcstas_style.css' />";
	print $f "<script type=\"text/javascript\"\n", 
	         "mcstas_vgrid=\"$mcstas_vgrid\";\n</script>";
	foreach $lib (@jquery_libs) {
	    print $f "<script type=\"text/javascript\" src=\"", 
	             $jquery_path, "/", $lib, "\"></script>\n";
	}
	print $f "</HEAD>\n\n";
	print $f "<BODY>\n";
    }

    print $f "<div class='mcstas_instrument'>\n";
    print $f "<H1>The <CODE>$d->{'name'}</CODE> $d->{'type'}</H1>\n\n";
    print $f "$d->{'identification'}{'short'}\n\n";

    print $f "<div class='id'>\n";
    print $f "<H2><A NAME=id></A>Identification</H2>\n";
    print $f "\n<UL>\n";
    print $f "  <LI> <B>Site:   $d->{'site'}</B>\n";
    print $f "  <LI> <B>Author:</B>$d->{'identification'}{'author'}</B>\n";
    print $f "  <LI> <B>Origin:</B>$d->{'identification'}{'origin'}</B>\n";
    print $f "  <LI> <B>Date:</B>$d->{'identification'}{'date'}</B>\n";
    print $f "  <LI> <B>Version:</B>$d->{'identification'}{'version'}</B>\n";
    if(@{$d->{'identification'}{'history'}}) {
	my $entry;
	print $f "  <LI> <B>Modification history:</B> <UL>\n";
	for $entry (@{$d->{'identification'}{'history'}}) {
	    print $f "    <LI> $entry\n";
	}
	print $f "  </UL>\n";
    }
    print $f "</UL>\n";
    print $f "</div>\n";

    print $f "\n<div class='ipar'>\n";
    print $f "\n<H2><A NAME=ipar></A>Job submission</H2>\n";

    # use original file name for IDs in the generated html form (below)
    # cut away the suffix (match has been checked before)
    $n =~ s/\.instr$//; 
    gen_submission_form($f, $d->{'inputpar'}, $d->{'parhelp'}, $n); 

    print $f "</div>\n";

    if($d->{'description'}) {
	print $f "<div class='desc'>\n";
	print $f "<H2><A NAME=desc></A>Description</H2>\n";
	print $f "\n<PRE>\n$d->{'description'}</PRE>\n";
	print $f "</div>\n";
    }

    print $f "</div> <!-- mcstas instrument -->\n";
   if ( !$content_only ) {
    print $f "</BODY></HTML>\n";
   }
    close $f;
    
}

# Start of main ===============================

my $file;
my $basename;
my $base="";

for($i = 0; $i < @ARGV; $i++) {
  $_ = $ARGV[$i];
  # Options for html generation
  if(/^--help$/i || /^-h$/i ) {
      print "Usage: $0 [options] <instrument file>\n";
      print "Generate html for an instrument, to submit MiG jobs later.\n";
      print "   -h      , --help          Show this help\n";
      print "   -d      , --verbose       verbose output\n";
      print "           , --content-only  suppress html prefix/suffix\n";

      print "   -o <name>                 set output name (default: <input basename>.html\n";
#      print "   -s <dns> , --server=<dns> set fully qualified DNS name of MiG server to target\n";
      print "   -v <name>, --vgrid=<name> set name of the VGrid on the MiG server\n";
      print "(used in generated html)";
      print "\n";
      print "This script is an adaption of mcdoc to specific purposes.\n";
      print "Also see: http://www.mcstas.org.\n";
      exit;
  } elsif(/^-d$/i) {
      $verbose = 1;
  } elsif(/^--verbose$/i) {
      $verbose = 1;
  } elsif(/^-p$/i) {
      $verbose = -1;
  } elsif(/^--params$/i) {
      $verbose = -1;
  } elsif(/^--content-only$/i) {
      $content_only = 1;
  } elsif(/^-o$/i) {
      $basename = $ARGV[++$i];
#  } elsif(/^-s$/i) {
#      $mig_dns = $ARGV[++$i];
#  } elsif(/^--server=(.+)$/i ) {
#      $mig_dns = $1;
  } elsif(/^-v$/i) {
      $mcstas_vgrid = $ARGV[++$i];
  } elsif(/^--vgrid=(.+)$/i ) {
      $mcstas_vgrid = $1;
  } else {
      if (defined($file)) {
	  complain("Too many arguments.");
      }
      $file = $ARGV[$i];
  }
} # end for

#debug
if ($verbose > 0) {
    print "mcstas vgrid is ", $mcstas_vgrid, "\n";
#    print "MiG server is ", $mig_dns, "\n";
    print "instrument file is ", $file, "\n";
    print "instrument file is ", $file, "\n";
}

#if ( $mig_dns =~ /(https?:)|[\/]/i ) {
#    complain ("Problem with this server url\n" .
#	      "($mig_dns: contains http or slash)");
#}

if (!(defined($file))) {
    complain ("No file name given.");
}
if ($file !~ /^(.*)\.instr$/) {
    complain("seems $file is not an instrument file (*.instr)");
} 

if (!(defined($basename))) {
# grab the name without extension from the match above
    $basename = $1;
} elsif ($basename =~ /(.*).html$/ ) {
# cut erroneous html suffix from basename (will be added again later)
    $basename = $1;
}

if (!(-f "$file")) {
    complain("File $file does not exist.");
}

$data = component_information($file);
if (not defined($data)) {
    complain("Failed to get information for instrument '$file'");
}

# DEBUG
if ( $verbose > 0) {
    print STDOUT "$0: generating submission page for $file, in $basename.html\n";
}

$data->{'path'} = $file;

gen_html_description($data, $basename, $file);

if ( $verbose < 0 ) {
    print STDOUT $params;
}
if ( $verbose > 0) {
    print STDOUT "$0 finished\n";
}
