

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c a)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on d b))
)
)


