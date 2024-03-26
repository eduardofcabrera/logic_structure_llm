

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(ontable c)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a c)
(on b a)
(on c d)
(on e b))
)
)


