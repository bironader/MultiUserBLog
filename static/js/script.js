
editPostButton = function(){
	$(".edit-blog").click(function(){

	subject=$(this).find(".subject").html();
	artical=$(this).find(".blog").html();
	blog_id=$(this).find(".blog-id").text();
	user_id=$(this).find(".user-id").text();
	$("#edit-modal input[name=user-id]").val(user_id);
	$("#edit-modal input[name=edit-subject]").val(subject);
	$("#edit-modal textarea[name=edit-artical]").val(artical);
	$("#edit-modal input[name=blog-id]").val(blog_id);
	$("#error-modal .modal-message").html("You can only edit or delete your posts");
	
});
}

deletePostButton = function(){
	$(".delete-blog").click(function(){

	
	blog_id=$(this).find(".blog-id").text();
	user_id=$(this).find(".user-id").text();
	$("#warning-modal input[name=blog-id]").val(blog_id);
	$("#warning-modal input[name=user-id]").val(user_id);
	$("#error-modal .modal-message").html("You can only edit or delete your posts");
	
	
});
}
	

editCommentButton = function(){
	$(".edit-comment").click(function(){
		
		
	comment_id=$(this).find(".comment-id").text();
	comment=$(this).find(".comment").html();
	user_id=$(this).find(".user-id").text();	
	$("#editcomment-modal input[name=user-id]").val(user_id);
	$("#editcomment-modal input[name=comment-id]").val(comment_id);
	$("#editcomment-modal textarea[name=edit-comment]").val(comment);
	$("#error-modal .modal-message").html("You can only edit or delete your comments");
	
	

});
}
deleteCommentButton = function(){
	$(".delete-comment").click(function(){
	
	comment_id=$(this).find(".comment-id").text();
	user_id=$(this).find(".user-id").text();	
	$("#warning-modal input[name=user-id]").val(user_id);
	$("#warning-modal input[name=comment-id]").val(comment_id);	
	$("#error-modal .modal-message").html("You can only edit or delete your comments");
	$("#warning-modal  .modal-warning-msg").html("Are you sure you want delete this comment ?");
	$("#warning-modal .confirm").attr("name","delete-comment");
	
});
}	



$(document).ready(function(){
		editPostButton();
		deletePostButton();
		editCommentButton();
		deleteCommentButton();
		
})