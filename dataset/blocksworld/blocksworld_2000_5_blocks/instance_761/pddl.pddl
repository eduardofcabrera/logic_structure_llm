

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a e)
(on d a)
(on e b))
)
)


