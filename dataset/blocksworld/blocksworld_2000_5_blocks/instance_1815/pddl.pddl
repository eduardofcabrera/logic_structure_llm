

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(ontable c)
(on d c)
(ontable e)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on c a)
(on e b))
)
)


