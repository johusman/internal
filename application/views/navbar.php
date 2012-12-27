<div class="navbar navbar-inverse navbar-fixed-top">
	<div class="navbar-inner">
		<div class="container-fluid">
			<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</a>
			
			<a class="brand" href="/">Makerspace</a>

			<div class="nav-collapse collapse">
				<p class="navbar-text pull-right">Logged in as <a href="/user"><?php echo $this->User_model->get_user()->email; ?></a> | <a href="/auth/logout">Log out</a></p>
				
				<ul class="nav">
					<li><a href="/users">Members</a></li>
					<li><a href="/newsletter">Newsletter</a></li>
					<li><a href="/todo">ToDo</a></li>
					<li><a href="/admin">Admin</a></li>
					<li class="active"><a href="/debug">Debug</a></li>
				</ul>
			</div><!--/.nav-collapse -->
		</div>
	</div>
</div>
