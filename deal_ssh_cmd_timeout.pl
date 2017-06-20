#! /usr/bin/perl
use warnings;
use strict;
use Expect;
use diagnostics;


my $pid = fork();

if ($pid) {
	print "Started child process id: $pid\n";
} elsif ($pid == 0) {
	cmd("bash /home/automation/test.sh");
	exit $?;
} else {
	print("fork error!");
	exit 1;
}
$SIG{TERM} = sub { kill TERM => $pid};
$SIG{INT} = sub { kill INT => $pid};

sleep(60);
my $status = -1;
kill TERM => $pid;
sleep 1 and kill INT => $pid if kill 0 => $pid;
sleep 1 and kill KILL => $pid if kill 0 => $pid;
exit $status;
#print "Waiting for the child process to complete...\n";
#waitpid ($pid, 0);
#print "The child process has finished executing.\n\n";

sub cmd {
my $exp = new Expect;
my $cmd = shift;
my $timeout = 10;
$exp->raw_pty(1);
$exp->log_user(0);
$exp->spawn("ssh root\@10.138.25.141 -p 22");
$exp->expect($timeout,
               [
                qr'login: $',
                sub {
                  my $fh = shift;
                  $fh->send("automation\r");
                  exp_continue;
                }
               ],
               [
                '[Pp]assword: $',
                sub {
                  my $fh = shift;
                  print $fh "password\r";
                  exp_continue;
                }
               ],
               [
                eof =>
                sub {
                    #die "ERROR: premature EOF in login.\n";
		    die "no password prompt: $! --- $@\n";
                }
               ],
               [
                timeout =>
                sub {
                  die "No login.\n";
                }
               ],
               '-re', qr'[#>:] $', #' wait for shell prompt, then exit expect
              );
print("$cmd ..");
$| = 1;
$exp->send("$cmd \r");
	my ($matched_pattern_position,
				 $error,
				 $successfully_matching_string,
				 $before_match,
				 $after_match) =
$exp->expect($timeout,
               [
                '[Pp]assword: $',
                sub {
                  my $fh = shift;
                  print $fh "password\n";
                  exp_continue;
                }
               ],
               [
                timeout =>
                sub {
                  die "did not find prompt.\n";
                }
               ],
               '-re', qr'[#>:] $', #' wait for shell prompt, then exit expect
              );
#print "<<<1.$error \n"."2.$before_match \n"."3.$successfully_matching_string \n"."4.$after_match>>> \n";
print($before_match);
}
