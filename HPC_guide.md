# DTU HPC #

## Connect ##

Open terminal and write following line with your student number:

    ssh <YOUR_STUDENT_NUMBER>@login2.gbar.dtu.dk

You will be asked for a password. Use your password for inside and learn.

## Git ##

Locate yourself in a folder where you want the repository to be located by using:

    cd <FOLDER_PATH>

Clone the repository from github by using following line for ssh:

    git clone git@github.com:Gylling/DeepLearning.git

And for url:

    git clone https://github.com/Gylling/DeepLearning.git

Make sure that you've generated an ssh key on the server if you choose to go with ssh. 
You can find info on generating a ssh key on [GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).


## Edit .bashrc file ##

You can open .bashrc in nano from any folder with:

    nano ~/.bashrc

This will open the file in nano. Delete all the content and paste the folling code into it.

    # User .bashrc file.                                            UNI-C 25/07-96
    #
    # GNU Bourne Again SHell (bash) initialization.
    # You are expected to edit this file to meet your own needs.
    #
    # The commands in this file are executed
    # each time a new bash shell is started.
    #

    # Source the shared .bashrc file if it exists.
    if [ -r /.bashrc ] ; then . /.bashrc ; fi

    # Place your own code within the if-fi below to
    # avoid it being executed on logins via remote shell,
    # remote exec, batch jobs and other non-interactive logins.

    # Set up the bash environment if interactive login.
    if tty -s ; then

    # Set the system prompt.
    PS1="\w\n\h(\u) $ "
    export PS1

    # Set up some user command aliases.
    alias h=history
    alias source=.

    # Confirm before removing, replacing or overwriting files.
    alias rm="rm -i"
    alias mv="mv -i"
    alias cp="cp -i"

    fi

    # Place your own code within the if-fi above to
    # avoid it being executed on logins via remote shell,
    # remote exec, batch jobs and other non-interactive logins.

    module load python3/3.7.11
    module swap cuda/11.3
    module swap cudnn/v8.2.0.53-prod-cuda-11.3
    module load ffmpeg/4.2.2
    pip3 install --user torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
    pip3 install --user procgen
    pip3 install --user imageio

Use **Crtl+X** followed by **y** and then **Enter** to save the changes and exit nano.

Now reload your module by:

     source ~/.bashrc

## Push a job to queue ##

Now you are ready to push a job to the queue. 
**jobscript.sh** defines the job that we need for now. You can find information on the files content at [DTU-HPS's website for jobscripts](https://www.hpc.dtu.dk/?page_id=1416)

You push the job to the queue by using following command - make sure to be in the folder of the repository:

    bsub < jobScript.sh

You can get the status of the job by using:

    bstat

You can kill the job by using:

    bkill <JOB_ID>


More information on managing jobs can be found at
[DTU-HPS's website for managing jobs](https://www.hpc.dtu.dk/?page_id=1519)